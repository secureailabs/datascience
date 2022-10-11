from typing import Dict

from sail_safe_functions_orchestrator.data_model.data_model_tabular import \
    DataModelTabular


class ReferenceDatasetTabular:
    def __init__(self, dataset_id: str, reference_id: str, data_model_tabular: DataModelTabular) -> None:
        self.dataset_id = dataset_id
        self.reference_id = reference_id
        self.data_model_tabular = data_model_tabular

    def to_dict(self):
        dict = {}
        dict["__type__"] = "ReferenceDatasetTabular"
        dict["dataset_id"] = self.dataset_id
        dict["reference_id"] = self.reference_id
        dict["data_model_tabular"] = self.data_model_tabular.to_dict()
        return dict

    @staticmethod
    def from_dict(dict: Dict):
        if dict["__type__"] != "ReferenceDatasetTabular":
            raise ValueError(f"Incorrect __type__ in dict {dict}")
            
        return ReferenceDatasetTabular(
            dict["dataset_id"], dict["reference_id"], DataModelTabular.from_dict(dict["data_model_tabular"])
        )
