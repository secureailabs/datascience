from sail_safe_functions_orchestrator.data_model.data_model_data_frame import DataModelDataFrame


class ReferenceDataFrame:
    def __init__(self, dataset_id: str, reference_id: str, data_model_data_frame: DataModelDataFrame) -> None:
        self.dataset_id = dataset_id
        self.reference_id = reference_id
        self.data_model_data_frame = data_model_data_frame
