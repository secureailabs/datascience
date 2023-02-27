import pytest
from sail_safe_functions.aggregator.statistics.student_t_test import StudentTTest
from sail_safe_functions.test.helper_sail_safe_functions.generator_two_sample_float import GeneratorTwoSampleFloat
from sail_safe_functions.test.helper_sail_safe_functions.tools_accuracy import (
    experiment_bias_variance_two_sample,
    plot_experiment_bias_variance_two_sample_hist,
)


@pytest.mark.active
def test_experiment_accuracy():
    generator = GeneratorTwoSampleFloat(
        "uniform unit",
        type_distribution="uniform",
        mean=0.0,
        standard_deviation=1.0,
        list_weight_federation=[0.25, 0.25, 0.25, 0.25],
        resolution=0.1,
    )

    import os

    # load every test dataset
    from sail_safe_functions.aggregator.data_frame_federated import DataFrameFederated
    from sail_safe_functions.aggregator.data_model.data_model_series import DataModelSeries
    from sail_safe_functions.aggregator.series_federated import SeriesFederated
    from sail_safe_functions.aggregator.statistics.pearson import Pearson
    from sail_safe_functions.test.helper_sail_safe_functions.tools_data_test import ToolsDataTest

    sample_size = 15
    effect_size = 1.0
    is_paired = True
    significance = 0.05
    run_count = 200

    estimator = Pearson(alternative="two-sided")
    target_estimate_name = estimator.list_estimate_name[0]
    experiment = experiment_bias_variance_two_sample(
        estimator,
        generator,
        sample_size,
        effect_size,
        is_paired,
        significance,
        run_count,
        target_estimate_name,
    )
    list_experiment = [experiment]
    plot_experiment_bias_variance_two_sample_hist(list_experiment, do_show=False)
