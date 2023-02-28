from sail_core.tools_common import check_instance
from sail_safe_functions.aggregator.data_model.data_model_data_frame import DataModelDataFrame
from sail_safe_functions.aggregator.reference_data_frame import ReferenceDataFrame
from sail_safe_functions.aggregator.reference_dataset_longitudinal import ReferenceDatasetLongitudinal
from sail_safe_functions.aggregator.service_reference import ServiceReference
from sail_safe_functions.safe_function_base import SafeFunctionBase


class ConvertToDataFramePrecompute(SafeFunctionBase):
    # TODO this might be in the wrong spot, is this a convert function?
    @staticmethod
    def run(
        reference_dataset_logitudinal: ReferenceDatasetLongitudinal,
        data_model_data_frame: DataModelDataFrame,
    ) -> ReferenceDataFrame:
        check_instance(reference_dataset_logitudinal, ReferenceDatasetLongitudinal)
        check_instance(data_model_data_frame, DataModelDataFrame)

        dataset_logitudinal = ServiceReference.get_instance().reference_to_dataset_longitudinal(
            reference_dataset_logitudinal
        )
        data_frame = dataset_logitudinal.convert_to_data_frame(data_model_data_frame)
        return ServiceReference.get_instance().data_frame_to_reference(data_frame)
