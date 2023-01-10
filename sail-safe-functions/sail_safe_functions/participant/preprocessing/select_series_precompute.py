from sail_safe_functions.aggregator.reference_data_frame import ReferenceDataFrame
from sail_safe_functions.aggregator.reference_series import ReferenceSeries
from sail_safe_functions.aggregator.service_reference import ServiceReference
from sail_safe_functions.safe_function_base import SafeFunctionBase


class SelectSeriesPrecompute(SafeFunctionBase):
    @staticmethod
    def run(
        reference: ReferenceDataFrame,
        series_name: str,
    ) -> ReferenceSeries:
        data_frame = ServiceReference.get_instance().reference_to_data_frame(reference)
        series = data_frame[series_name]
        return ServiceReference.get_instance().series_to_reference(series)
