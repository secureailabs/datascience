from typing import Dict

from sail_safe_functions_orchestrator.data_model.data_model_series import DataModelSeries
from sail_safe_functions_orchestrator.tools_common import check_instance

class ReferenceSeries:
    def __init__(self, dataset_id: str, reference_id: str, data_model_series: DataModelSeries) -> None:
        check_instance(dataset_id, str)
        check_instance(reference_id, str)
        check_instance(data_model_series, DataModelSeries)
        self.dataset_id = dataset_id
        self.reference_id = reference_id
        self.data_model_series = data_model_series

    def to_dict(self):
        dict = {}
        dict["__type__"] = "ReferenceSeries"
        dict["dataset_id"] = self.dataset_id
        dict["reference_id"] = self.reference_id
        dict["data_model_series"] = self.data_model_series.to_dict()
        return dict

    @staticmethod
    def from_dict(dict: Dict):
        if dict["__type__"] != "ReferenceSeries":
            raise ValueError(f"Incorrect __type__ in dict {dict}")

        return ReferenceSeries(
            dict["dataset_id"], dict["reference_id"], DataModelSeries.from_dict(dict["data_model_series"])
        )
