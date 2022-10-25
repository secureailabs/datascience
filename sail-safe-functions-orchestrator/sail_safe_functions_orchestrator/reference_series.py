from sail_safe_functions_orchestrator.data_model.data_model_series import DataModelSeries


class ReferenceSeries:
    def __init__(self, reference_id: str, data_model_series: DataModelSeries) -> None:
        self.reference_id = reference_id
        self.data_model_series = data_model_series
