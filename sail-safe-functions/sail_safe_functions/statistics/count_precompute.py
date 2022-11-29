from sail_safe_functions.safe_function_base import SafeFunctionBase
from sail_safe_functions_orchestrator.reference_series import ReferenceSeries
from sail_safe_functions_orchestrator.service_reference import ServiceReference
from sail_safe_functions_orchestrator.tools_common import (
    check_empty_series,
    check_instance,
    check_series_nan,
    check_series_one_value,
)


class CountPrecompute(SafeFunctionBase):

    """
    Precomputes data for computing the count
    """

    @staticmethod
    def run(
        sample_0_series: ReferenceSeries,
    ) -> float:
        sample_0 = ServiceReference.get_instance().reference_to_series(sample_0_series).to_numpy()
        check_instance(sample_0_series, ReferenceSeries)
        check_empty_series(sample_0)
        check_series_nan(sample_0)
        check_series_one_value(sample_0)
        return sample_0.size
