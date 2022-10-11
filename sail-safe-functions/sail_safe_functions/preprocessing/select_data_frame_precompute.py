from sail_safe_functions_orchestrator.reference_data_frame import ReferenceDataFrame
from sail_safe_functions_orchestrator.reference_dataset_tabular import ReferenceDatasetTabular
from sail_safe_functions_orchestrator.service_reference import ServiceReference
from sail_safe_functions.safe_function_base import SafeFunctionBase

class SelectDataFramePrecompute(SafeFunctionBase):
    def run(reference: ReferenceDatasetTabular, data_frame_name: str) -> ReferenceDataFrame:
        dataset_tabular = ServiceReference.get_instance().reference_to_dataset_tabular(reference)
        data_frame = dataset_tabular[data_frame_name]
        return ServiceReference.get_instance().data_frame_to_reference(data_frame)
