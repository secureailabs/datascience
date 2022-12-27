from typing import List, Tuple

import numpy
from sail_safe_functions.aggregator import statistics
from sail_safe_functions.aggregator.series_federated import SeriesFederated
from sail_safe_functions.participant.preprocessing.cdf_precompute import CumulativeDistributionFunctionPrecompute
from scipy import interpolate


def cumulative_distribution_function(sample_0: SeriesFederated) -> Tuple[List[float], List[float]]:
    """Computes a CDF by aproximation with at least the square root of the sample
    size equally spaced between a estimate of the min and the max

    :param sample_0: The federated series over which the cdf should be computed
    :type sample_0: SeriesFederated
    :return: returns two lists of floating point values representing the domain and the values of the cdf
    :rtype: Tuple[List[float], List[float]]
    """
    return CumulativeDistributionFunction.run(sample_0)


class CumulativeDistributionFunction:
    "Estimator for non-disclosive CDF"

    @staticmethod
    def run(
        sample_0: SeriesFederated,
    ) -> Tuple[List[float], List[float]]:

        domain_min, domain_max = statistics.min_max(sample_0)
        list_precompute = sample_0.map_function(CumulativeDistributionFunctionPrecompute, domain_min, domain_max)

        return CumulativeDistributionFunction.aggregate(list_precompute, domain_min, domain_max)

    @staticmethod
    def aggregate(
        list_precompute: List[Tuple[List[float], List[float], int]],
        domain_min,
        domain_max,
    ) -> Tuple[List[float], List[float]]:
        list_array_value_resampled = []
        count_total = 0
        for precompute in list_precompute:
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
