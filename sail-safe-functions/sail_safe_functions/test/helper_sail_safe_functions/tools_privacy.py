import numpy
from sail_safe_functions.aggregator import statistics
from sail_safe_functions.aggregator.series_federated import SeriesFederated
from sail_safe_functions.aggregator.statistics.estimator_one_sample import EstimatorOneSample
from sail_safe_functions.test.helper_sail_safe_functions.tools_data_test import (
    series_drop_by_index,
    series_split_random,
)


def compute_single_knockout_privacy_measure(
    estimator: EstimatorOneSample,
    series_0: SeriesFederated,
):
    estimate_full = numpy.array(estimator.run(series_0))
    error_abs_max = numpy.zeros(estimate_full.shape)
    sample_size = statistics.count((series_0))
    for i in range(sample_size):
        series_0_single_knockout = series_drop_by_index(series_0, i)

        estimate_single_knockout = numpy.array(estimator.run(series_0_single_knockout))
        error_abs = numpy.abs(estimate_full - estimate_single_knockout)
        error_abs_max = numpy.maximum(error_abs_max, error_abs)
    return error_abs_max


def experiment_privacy_one_sample_dma(
    estimator: EstimatorOneSample,
    series_0: SeriesFederated,
    extract_fraction: float,
    run_count: int,
) -> dict:
    ### perfroms a number of automated Divergence Membership Attacks and sees how many pass
    # divergence is abs error

    if extract_fraction <= 0 or 1 < extract_fraction:
        raise Exception("extract fraction must be between 0 and 1")

    experiment = {}
    experiment["parameter"] = {}
    experiment["parameter"]["estimator_name"] = estimator.estimator_name
    experiment["parameter"]["series_name"] = series_0.series_name
    experiment["parameter"]["extract_fraction"] = extract_fraction
    experiment["parameter"]["run_count"] = run_count

    # TODO series should be of equal size
    size = statistics.count(series_0)
    size_series_a = size // 2
    size_series_b = size // 2
    size_series_e = int(size_series_a * extract_fraction)
    if size_series_e <= 0:
        size_series_e = 1

    break_count = 0
    for i in range(run_count):
        series_a, series_b = series_split_random(series_0, size_series_b)

        series_e, _ = series_split_random(series_a, size_series_e)
        if 1 < len(estimator.list_estimate_name):
            estimate_a = estimator.run(series_a)[0]
            estimate_b = estimator.run(series_b)[0]
            estimate_e = estimator.run(series_e)[0]
        else:
            estimate_a = estimator.run(series_a)
            estimate_b = estimator.run(series_b)
            estimate_e = estimator.run(series_e)
        # todo allow other divergence
        divergence_a = numpy.abs(estimate_a - estimate_e)
        divergence_b = numpy.abs(estimate_b - estimate_e)
        if divergence_a < divergence_b:
            break_count += 1

    fraction_hit = float(break_count) / float(run_count)
    experiment["result"] = {}
    experiment["result"]["fraction_hit"] = fraction_hit
    return experiment
