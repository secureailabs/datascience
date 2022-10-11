from typing import List, Tuple

import numpy
from sail_safe_functions.preprocessing.cdf_aggregate import (
    CumulativeDistributionFunctionAggregate,
)
from sail_safe_functions.preprocessing.cdf_precompute import (
    CumulativeDistributionFunctionPrecompute,
)
from sail_safe_functions_orchestrator.series_federated import SeriesFederated
from sail_safe_functions_orchestrator import statistics


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
    def run(sample_0: SeriesFederated) -> Tuple[List[float], List[float]]:

        domain_min, domain_max = statistics.min_max(sample_0)
        list_precompute = []
        for dataset_id in sample_0.list_dataset_id:  # TODO rework abcs
            client = sample_0.service_client.get_client(dataset_id)
            reference_series = sample_0.get_reference_series(dataset_id)
            list_precompute.append(client.call(
                CumulativeDistributionFunctionPrecompute,
                    reference_series, domain_min, domain_max
                )
            )
        return CumulativeDistributionFunctionAggregate.run(
            list_precompute, domain_min, domain_max
        )

    def run_reference(sample_0: SeriesFederated) -> Tuple[List[float], List[float]]:
        array_sample_0 = sample_0.to_numpy()
        array_domain = numpy.sort(array_sample_0)
        array_domain = numpy.insert(array_domain, 0, array_domain[0])

        array_value = numpy.arange(1, len(array_sample_0) + 1) / float(len(array_sample_0))
        array_value = numpy.insert(array_value, 0, 0)
        return array_domain.tolist(), array_value.tolist()
