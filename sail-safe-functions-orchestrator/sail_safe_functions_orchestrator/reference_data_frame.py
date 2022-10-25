from sail_safe_functions_orchestrator.data_model.data_model_data_frame import DataModelDataFrame


class ReferenceDataFrame:
    def __init__(self, reference_id: str, data_model_data_frame: DataModelDataFrame) -> None:
        self.reference_id = reference_id
        self.data_model_data_frame = data_model_data_frame
