import pytest
from sail_safe_functions.aggregator.statistics.student_t_test import StudentTTest
from sail_safe_functions.test.helper_sail_safe_functions.generator_two_sample_float import GeneratorTwoSampleFloat
from sail_safe_functions.test.helper_sail_safe_functions.tools_accuracy import experiment_power, plot_experiment_power


@pytest.mark.active
def test_experiment_power():
    two_sample_uniform_low_res_fed = GeneratorTwoSampleFloat(
        "uniform unit",
        type_distribution="uniform",
        mean=0.0,
        standard_deviation=1.0,
        list_weight_federation=[0.25, 0.25, 0.25, 0.25],
        resolution=0.1,
    )

    sample_size = 10
    effect_size = 0.1
    is_paired = False
    significance = 0.05
    run_count = 200

    estimator = StudentTTest(alternative="two-sided")

    # TODO convert this to a dataframe maybe
    list_list_list_experiment = []
    experiment = experiment_power(
        estimator, two_sample_uniform_low_res_fed, sample_size, effect_size, is_paired, significance, run_count
    )

    list_sample_size = [sample_size]
    list_list_list_experiment = [[[experiment]]]
    plot_experiment_power(list_sample_size, list_list_list_experiment)
