from typing import List, Tuple

import numpy
from sail_safe_functions.preprocessing.cdf_agregate import CdfAgregate
from sail_safe_functions.preprocessing.cdf_precompute import CdfPrecompute
from sail_safe_functions_orchestrator.series_federated import SeriesFederated
from sail_safe_functions_orchestrator.statistics.min_max_federate import MinMaxFederate


class CdfFederate:
    @staticmethod
    def run(sample_0: SeriesFederated) -> Tuple[List[float], List[float]]:
        domain_min, domain_max = MinMaxFederate.run(sample_0)

        list_precompute = []
        for series in sample_0.dict_series.values():  # TODO rework abcs
            list_precompute.append(CdfPrecompute.run(series, domain_min, domain_max))
        list_domain, list_value = CdfAgregate.run(list_precompute, domain_min, domain_max)

        return list_domain, list_value

    def run_reference(sample_0: SeriesFederated) -> Tuple[List[float], List[float]]:
        array_sample_0 = sample_0.to_numpy()
        array_domain = numpy.sort(array_sample_0)
        array_domain = numpy.insert(array_domain, 0, array_domain[0])

        array_value = numpy.arange(1, len(array_sample_0) + 1) / float(len(array_sample_0))
        array_value = numpy.insert(array_value, 0, 0)
        return array_domain.tolist(), array_value.tolist()
