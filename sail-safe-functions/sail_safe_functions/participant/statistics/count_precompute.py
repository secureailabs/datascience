from sail_core.tools_common import check_instance
from sail_safe_functions.aggregator.reference_series import ReferenceSeries
from sail_safe_functions.aggregator.service_reference import ServiceReference
from sail_safe_functions.aggregator.tools_common import check_empty_series, check_series_nan, check_series_one_value
from sail_safe_functions.safe_function_base import SafeFunctionBase


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
        # check_empty_series(sample_0) # TODO move check to agregator
        check_series_nan(sample_0)
        return sample_0.size
