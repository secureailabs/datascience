from typing import List, Tuple

import numpy
from sail_safe_functions.safe_function_base import SafeFunctionBase
from sail_safe_functions_orchestrator.reference_series import ReferenceSeries
from sail_safe_functions_orchestrator.service_reference import ServiceReference
from scipy import interpolate


class CumulativeDistributionFunctionPrecompute(SafeFunctionBase):
    """
    Precomputes data for creating a federated 1dcdf
    """

    def run(
        series_0_reference: ReferenceSeries, domain_min: float, domain_max: float
    ) -> Tuple[List[float], List[float], int]:
        # TODO test this for series of size 1

        array_sample_0 = ServiceReference.get_instance().reference_to_series(series_0_reference).to_numpy()
        size_sample_0 = len(array_sample_0)
        if size_sample_0 == 1:
            array_domain_safe = numpy.array([array_sample_0[0], array_sample_0[0]])
            array_value_safe = numpy.array([0, 1])
        else:
            count_value = int(numpy.ceil(numpy.sqrt(len(array_sample_0))))

            array_domain = numpy.sort(array_sample_0)
            array_domain = numpy.insert(array_domain, 0, domain_min)
            array_domain = numpy.insert(array_domain, -1, domain_max)
            array_value = numpy.arange(1, size_sample_0 + 1) / float(size_sample_0)
            array_value = numpy.insert(array_value, 0, 0)
            array_value = numpy.insert(array_value, -1, 1)

            array_domain_safe = numpy.linspace(domain_min, domain_max, count_value)
            array_value_safe = interpolate.interp1d(array_domain, array_value)(array_domain_safe)
        return array_domain_safe.tolist(), array_value_safe.tolist(), size_sample_0
