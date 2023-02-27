import pytest
from sail_safe_functions.aggregator import statistics
from sail_safe_functions.aggregator.series_federated import SeriesFederated
from sail_safe_functions.aggregator.statistics.min_max import MinMax
from sail_safe_functions.test.helper_sail_safe_functions.generator_one_sample_float import GeneratorOneSampleFloat
from sail_safe_functions.test.helper_sail_safe_functions.tools_privacy import (
    experiment_privacy_one_sample_dma,
    plot_experiment_privacy_one_sample_dma,
)


@pytest.mark.active
def test_experiment_privacy(one_sample_big: SeriesFederated):
    # TODO this generators shows some intresting problems that we should investigate
    # generator = GeneratorOneSampleFloat(
    #     "uniform unit",
    #     type_distribution="uniform",
    #     mean=0.0,
    #     standard_deviation=1.0,
    #     list_weight_federation=[0.25, 0.25, 0.25, 0.25],
    #     resolution=0.1,
    # )

    # sample_size = 10

    extraction_factor = 0.1
    run_count = 10

    estimator = MinMax()

    # TODO convert this to a dataframe maybe
    experiment = experiment_privacy_one_sample_dma(estimator, one_sample_big, extraction_factor, run_count)

    list_list_experiment = [[experiment]]
    plot_experiment_privacy_one_sample_dma(list_list_experiment, do_show=False)
