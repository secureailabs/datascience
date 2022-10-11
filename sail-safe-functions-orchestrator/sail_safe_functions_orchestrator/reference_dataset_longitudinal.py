from typing import Dict

from sail_safe_functions_orchestrator.data_model.data_model_longitudinal import DataModelLongitudinal


class ReferenceDatasetLongitudinal:
    #TODO datahiding
    def __init__(self, dataset_id: str, reference_id: str, data_model_longitudinal: DataModelLongitudinal) -> None:
        self.dataset_id = dataset_id
        self.reference_id = reference_id
        self.data_model_logitudinal = data_model_longitudinal #TODO type

    def to_dict(self):
        dict = {}
        dict["__type__"] = "ReferenceDatasetLongitudinal"
        dict["dataset_id"] = self.dataset_id
        dict["reference_id"] = self.reference_id
        dict["data_model_longitudinal"] = self.data_model_logitudinal.to_dict()
        return dict

    @staticmethod
    def from_dict(dict: Dict):
        if dict["__type__"] != "ReferenceDatasetLongitudinal":
            raise ValueError(f"Incorrect __type__ in dict {dict}")
            
        return ReferenceDatasetLongitudinal(
            dict["dataset_id"], dict["reference_id"], DataModelLongitudinal.from_dict(dict["data_model_longitudinal"])
        )
