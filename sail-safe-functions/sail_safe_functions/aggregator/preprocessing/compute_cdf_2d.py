from typing import List, Tuple

import numpy
from sail_safe_functions.aggregator import statistics
from sail_safe_functions.aggregator.data_frame_federated import DataFrameFederated
from sail_safe_functions.aggregator.preprocessing.cumulative_distribution_function import CumulativeDistributionFunction
from sail_safe_functions.aggregator.series_federated import SeriesFederated
from sail_safe_functions.participant.preprocessing.cdf_precompute import CumulativeDistributionFunctionPrecompute
from scipy import interpolate


def compute_cumulative_distribution_function_2d(
    data_frame: DataFrameFederated,
    series_name_0: str,
    series_name_1: str,
) -> CumulativeDistributionFunction:
    """
    _summary_

    :param data_frame: data frame from which to source the series
    :type data_frame: DataFrameFederated
    :param series_name_0: name of series 0
    :type series_name_0: str
    :param series_name_1: name of series 1
    :type series_name_1: str
    :return: returns a CumulativeDistributionFunction object representing the underlying data
    :rtype: CumulativeDistributionFunction
    """
    return ComputeCumulativeDistributionFunction2D.run(data_frame, series_name_0, series_name_1)


class ComputeCumulativeDistributionFunction2D:
    "Estimator for non-disclosive CDF"

    @staticmethod
    def run(
        data_frame: DataFrameFederated,
        series_name_0: str,
        series_name_1: str,
    ) -> CumulativeDistributionFunction:
        if series_name_0 not in data_frame.list_series_name:
            raise ValueError(
                f"No series with name {series_name_0} in data_frame with name {data_frame.data_frame_name}"
            )
        if series_name_1 not in data_frame.list_series_name:
            raise ValueError(
                f"No series with name {series_name_0} in data_frame with name {data_frame.data_frame_name}"
            )

        sample_0 = data_frame[series_name_0]
        sample_1 = data_frame[series_name_1]
        domain_min_0, domain_max_0 = statistics.min_max(sample_0)
        domain_min_1, domain_max_1 = statistics.min_max(sample_1)
        list_cdf: List[CumulativeDistributionFunction] = sample_0.map_function(
            ComputeCumulativeDistributionFunction2DPrecompute, domain_min_0, domain_max_0, domain_min_1, domain_max_1
        )

        list_array_value_resampled = []
        count_total = 0
        for precompute in list_cdf:
            count_total += precompute[2]
        count_value = int(numpy.ceil(numpy.sqrt(count_total)))

        array_domain_resampled = numpy.linspace(domain_min, domain_max, count_value)
        list_weight = []
        for precompute in list_precompute:
            list_weight.append(precompute[2] / count_total)
            list_array_value_resampled.append(
                interpolate.interp1d(precompute[0], precompute[1])(array_domain_resampled)
            )

        array_weight = numpy.array(list_weight)
        array_value_resampled = numpy.matmul(numpy.vstack(list_array_value_resampled).T, array_weight)

        return array_domain_resampled.tolist(), array_value_resampled.tolist()

    @staticmethod
    def run_reference(
        sample_0: SeriesFederated,
    ) -> Tuple[List[float], List[float]]:
        array_sample_0 = sample_0.to_numpy()
        array_domain = numpy.sort(array_sample_0)
        array_domain = numpy.insert(array_domain, 0, array_domain[0])

        array_value = numpy.arange(1, len(array_sample_0) + 1) / float(len(array_sample_0))
        array_value = numpy.insert(array_value, 0, 0)
        return array_domain.tolist(), array_value.tolist()
