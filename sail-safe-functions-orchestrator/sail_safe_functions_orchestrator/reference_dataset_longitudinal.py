from sail_safe_functions_orchestrator.data_model.data_model_longitudinal import DataModelLongitudinal


class ReferenceDatasetLongitudinal:
    def __init__(self, dataset_id: str, data_model_logitudinal: DataModelLongitudinal) -> None:
        self.dataset_id = dataset_id
        self.data_model_logitudinal = data_model_logitudinal
