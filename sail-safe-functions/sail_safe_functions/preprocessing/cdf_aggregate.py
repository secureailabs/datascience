from typing import List, Tuple

import numpy
from scipy import interpolate


class CumulativeDistributionFunctionAggregate:
    """
    Aggregates data for a federated cdf
    """

    def run(
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
                interpolate.interp1d(precompute[0], precompute[1])(
                    array_domain_resampled
                )
            )

        array_weight = numpy.array(list_weight)
        array_value_resampled = numpy.matmul(
            numpy.vstack(list_array_value_resampled).T, array_weight
        )

        return array_domain_resampled.tolist(), array_value_resampled.tolist()
