from typing import List

from sail_safe_functions.aggregator.reference_data_frame import ReferenceDataFrame
from sail_safe_functions.aggregator.reference_series import ReferenceSeries
from sail_safe_functions.aggregator.service_reference import ServiceReference
from sail_safe_functions.safe_function_base import SafeFunctionBase


class SelectSubDataFramePrecompute(SafeFunctionBase):
    @staticmethod
    def run(
        reference: ReferenceDataFrame,
        list_series_name: List[str],
    ) -> ReferenceDataFrame:
        data_frame_source = ServiceReference.get_instance().reference_to_data_frame(reference)
        data_frame_target = data_frame_source.select_series(list_series_name)
        return ServiceReference.get_instance().data_frame_to_reference(data_frame_target)
