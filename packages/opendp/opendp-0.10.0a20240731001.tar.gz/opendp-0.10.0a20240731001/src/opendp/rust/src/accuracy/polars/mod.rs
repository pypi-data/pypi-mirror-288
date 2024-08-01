use opendp_derive::bootstrap;
use polars::{
    datatypes::{AnyValue, DataType, Field},
    frame::{row::Row, DataFrame},
    prelude::{IntoLazy, LazyFrame, Schema},
};
use polars_plan::{
    dsl::{AggExpr, Expr},
    plans::DslPlan,
};

#[cfg(test)]
mod test;

use crate::{
    accuracy::{
        discrete_gaussian_scale_to_accuracy, discrete_laplacian_scale_to_accuracy,
        gaussian_scale_to_accuracy, laplacian_scale_to_accuracy,
    },
    core::{Measure, Measurement, Metric, MetricSpace},
    domains::LazyFrameDomain,
    error::Fallible,
    measurements::{
        expr_noise::{Distribution, NoisePlugin, Support},
        expr_report_noisy_max::ReportNoisyMaxPlugin,
        is_threshold_predicate,
    },
    polars::{match_trusted_plugin, ExtractLazyFrame, OnceFrame},
    transformations::expr_discrete_quantile_score::match_discrete_quantile_score,
};

#[cfg(feature = "ffi")]
mod ffi;

#[bootstrap(
    name = "describe_polars_measurement_accuracy",
    features("contrib"),
    arguments(
        measurement(rust_type = "AnyMeasurement"),
        alpha(c_type = "AnyObject *", default = b"null")
    ),
    generics(MI(suppress), MO(suppress)),
    returns(c_type = "FfiResult<AnyObject *>")
)]
/// Get noise scale parameters from a measurement that returns a OnceFrame.
///
/// If a threshold is configured for censoring small/sensitive partitions,
/// a threshold column will be included,
/// containing the cutoff for the respective count query being thresholded.
///
/// # Arguments
/// * `measurement` - computation from which you want to read noise scale parameters from
/// * `alpha` - optional statistical significance to use to compute accuracy estimates
pub fn describe_polars_measurement_accuracy<MI: Metric, MO: 'static + Measure>(
    measurement: Measurement<LazyFrameDomain, OnceFrame, MI, MO>,
    alpha: Option<f64>,
) -> Fallible<DataFrame>
where
    (LazyFrameDomain, MI): MetricSpace,
{
    let schema = measurement.input_domain.schema();
    let lf = DataFrame::from_rows_and_schema(&[], &schema)?.lazy();
    let mut of = measurement.invoke(&lf)?;
    let lf: LazyFrame = of.eval_internal(&ExtractLazyFrame)?;

    lazyframe_utility(&lf, alpha)
}

struct UtilitySummary {
    pub name: String,
    pub aggregate: String,
    pub distribution: Option<String>,
    pub scale: Option<f64>,
    pub accuracy: Option<f64>,
    pub threshold: Option<u32>,
}

/// Get noise scale parameters from a LazyFrame.
///
/// # Arguments
/// * `lazyframe` - computation from which you want to read noise scale parameters from
/// * `alpha` - optional statistical significance to use to compute accuracy estimates
pub fn lazyframe_utility(lazyframe: &LazyFrame, alpha: Option<f64>) -> Fallible<DataFrame> {
    let mut utility = logical_plan_utility(&lazyframe.logical_plan, alpha, None)?;

    // only include the accuracy column if alpha is passed
    if alpha.is_none() {
        utility = utility.drop("accuracy")?;
    }
    // only include the threshold column if a threshold is set
    if utility.column("threshold")?.is_null().all() {
        utility = utility.drop("threshold")?;
    }
    Ok(utility)
}

fn logical_plan_utility(
    logical_plan: &DslPlan,
    alpha: Option<f64>,
    threshold: Option<(String, u32)>,
) -> Fallible<DataFrame> {
    match logical_plan {
        DslPlan::Select { expr: exprs, .. } | DslPlan::GroupBy { aggs: exprs, .. } => {
            let rows = exprs
                .iter()
                .map(|e| expr_utility(&e, alpha, threshold.clone()))
                .collect::<Fallible<Vec<Vec<UtilitySummary>>>>()?;

            Ok(DataFrame::from_rows_and_schema(
                &(rows.iter().flatten())
                    .map(|summary| {
                        Row(vec![
                            AnyValue::String(summary.name.as_ref()),
                            AnyValue::String(summary.aggregate.as_ref()),
                            match &summary.distribution {
                                Some(distribution) => AnyValue::String(distribution.as_ref()),
                                None => AnyValue::Null,
                            },
                            AnyValue::from(summary.scale),
                            AnyValue::from(summary.accuracy),
                            AnyValue::from(summary.threshold),
                        ])
                    })
                    .collect::<Vec<_>>(),
                &Schema::from_iter(vec![
                    Field::new("column", DataType::String),
                    Field::new("aggregate", DataType::String),
                    Field::new("distribution", DataType::String),
                    Field::new("scale", DataType::Float64),
                    Field::new("accuracy", DataType::Float64),
                    Field::new("threshold", DataType::UInt32),
                ]),
            )?)
        }
        DslPlan::Filter { input, predicate } => {
            let threshold = is_threshold_predicate(predicate.clone());
            logical_plan_utility(input.as_ref(), alpha, threshold)
        }
        DslPlan::Sort { input, .. }
        | DslPlan::Slice { input, .. }
        | DslPlan::Sink { input, .. } => logical_plan_utility(input.as_ref(), alpha, threshold),
        dsl => fallible!(FailedFunction, "unrecognized dsl: {:?}", dsl.describe()),
    }
}

fn expr_utility<'a>(
    expr: &Expr,
    alpha: Option<f64>,
    threshold: Option<(String, u32)>,
) -> Fallible<Vec<UtilitySummary>> {
    let name = expr.clone().meta().output_name()?.to_string();
    let expr = expr.clone().meta().undo_aliases();
    let t_value = threshold
        .clone()
        .and_then(|(t_name, t_value)| (name == t_name).then_some(t_value));

    if let Some((input, plugin)) = match_trusted_plugin::<NoisePlugin>(&expr)? {
        let accuracy = if let Some(alpha) = alpha {
            use {Distribution::*, Support::*};
            Some(match (plugin.distribution, plugin.support) {
                (Laplace, Float) => laplacian_scale_to_accuracy(plugin.scale, alpha),
                (Gaussian, Float) => gaussian_scale_to_accuracy(plugin.scale, alpha),
                (Laplace, Integer) => discrete_laplacian_scale_to_accuracy(plugin.scale, alpha),
                (Gaussian, Integer) => discrete_gaussian_scale_to_accuracy(plugin.scale, alpha),
            }?)
        } else {
            None
        };

        return Ok(vec![UtilitySummary {
            name,
            aggregate: expr_aggregate(&input[0])?.to_string(),
            distribution: Some(format!("{:?} {:?}", plugin.support, plugin.distribution)),
            scale: Some(plugin.scale),
            accuracy,
            threshold: t_value,
        }]);
    }

    if let Some((inputs, plugin)) = match_trusted_plugin::<ReportNoisyMaxPlugin>(&expr)? {
        return Ok(vec![UtilitySummary {
            name,
            aggregate: expr_aggregate(&inputs[0])?.to_string(),
            distribution: Some(format!("Gumbel{:?}", plugin.optimize)),
            scale: Some(plugin.scale),
            accuracy: None,
            threshold: t_value,
        }]);
    }

    match expr {
        Expr::Len => Ok(vec![UtilitySummary {
            name,
            aggregate: "Len".to_string(),
            distribution: None,
            scale: None,
            accuracy: alpha.is_some().then_some(0.0),
            threshold: t_value,
        }]),

        Expr::Function { input, .. } => Ok(input
            .iter()
            .map(|e| expr_utility(e, alpha, threshold.clone()))
            .collect::<Fallible<Vec<_>>>()?
            .into_iter()
            .flatten()
            .collect()),

        _ => fallible!(FailedFunction, "unrecognized primitive"),
    }
}

fn expr_aggregate(expr: &Expr) -> Fallible<&'static str> {
    if match_discrete_quantile_score(expr)?.is_some() {
        return Ok("Quantile");
    }
    Ok(match expr {
        Expr::Agg(AggExpr::Sum(_)) => "Sum",
        Expr::Len => "Len",
        expr => return fallible!(FailedFunction, "unrecognized aggregation: {:?}", expr),
    })
}
