import numpy
from sail_safe_functions.aggregator import statistics
from sail_safe_functions.aggregator.series_federated import SeriesFederated
from sail_safe_functions.aggregator.statistics.estimator import Estimator
from sail_safe_functions.test.helper_sail_safe_functions.tools_data_test import (
    series_drop_by_index,
    series_split_random,
)


def compute_single_knockout_privacy_measure(
    estimator: Estimator,
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


def create_report_dataset_membership_attack_absdiff(
    series_0: SeriesFederated,
    estimator: Estimator,
    extract_size: int,
    round_count: int,
):
    #  if extract_size <
    size = statistics.count(series_0)
    series_a, series_b = series_split_random(series_0, size // 2)
    series_e, _ = series_split_random(series_0, extract_size)

    break_count = 0
    for i in range(round_count):
        estimate_a = estimator.run(series_a)[0]
        estimate_b = estimator.run(series_b)[0]
        estimate_e = estimator.run(series_e)[0]
        if numpy.abs(estimate_a - estimate_e) < numpy.abs(estimate_b - estimate_e):
            break_count += 1
    return break_count / round_count
