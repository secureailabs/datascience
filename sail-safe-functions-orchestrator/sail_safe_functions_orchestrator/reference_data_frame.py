from typing import Dict

from sail_safe_functions_orchestrator.data_model.data_model_data_frame import DataModelDataFrame


class ReferenceDataFrame:
    def __init__(self, dataset_id: str, reference_id: str, data_model_data_frame: DataModelDataFrame) -> None:
        self.dataset_id = dataset_id
        self.reference_id = reference_id
        self.data_model_data_frame = data_model_data_frame

    def to_dict(self):
        dict = {}
        dict["__type__"] = "ReferenceDataFrame"
        dict["dataset_id"] = self.dataset_id
        dict["reference_id"] = self.reference_id
        dict["data_model_data_frame"] = self.data_model_data_frame.to_dict()
        return dict

    @staticmethod
    def from_dict(dict: Dict):
        if dict["__type__"] != "ReferenceDataFrame":
            raise ValueError(f"Incorrect __type__ in dict {dict}")

        return ReferenceDataFrame(
            dict["dataset_id"], dict["reference_id"], DataModelDataFrame.from_dict(dict["data_model_data_frame"])
        )
