from typing import List, Tuple

import numpy
from sail_safe_functions.preprocessing.cdf_agregate import CdfAgregate
from sail_safe_functions.preprocessing.cdf_precompute import CdfPrecompute
from sail_safe_functions_orchestrator.series_federated import SeriesFederated
from sail_safe_functions_orchestrator.statistics.min_max_federate import MinMaxFederate


class CdfFederate:
    "Estimator for non-disclosive CDF"

    @staticmethod
    def run(sample_0: SeriesFederated) -> Tuple[List[float], List[float]]:
        """Computes a CDF by aproximation with at least the square root of the sample
        size equally spaced between a estimate of the min and the max

        :param sample_0: The federated series over which the cdf should be computed
        :type sample_0: SeriesFederated
        :return: returns two lists of floating point values representing the domain and the values of the cdf
        :rtype: Tuple[List[float], List[float]]
        """
        domain_min, domain_max = MinMaxFederate.min_max(sample_0)

        list_precompute = []
        for series in sample_0.dict_series.values():  # TODO rework abcs
            list_precompute.append(CdfPrecompute.run(series, domain_min, domain_max))
        return CdfAgregate.run(list_precompute, domain_min, domain_max)

    def run_reference(sample_0: SeriesFederated) -> Tuple[List[float], List[float]]:
        array_sample_0 = sample_0.to_numpy()
        array_domain = numpy.sort(array_sample_0)
        array_domain = numpy.insert(array_domain, 0, array_domain[0])

        array_value = numpy.arange(1, len(array_sample_0) + 1) / float(len(array_sample_0))
        array_value = numpy.insert(array_value, 0, 0)
        return array_domain.tolist(), array_value.tolist()
