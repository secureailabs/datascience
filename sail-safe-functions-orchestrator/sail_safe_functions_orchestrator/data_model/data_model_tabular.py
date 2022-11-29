from typing import Dict, List

from sail_safe_functions_orchestrator.data_model.data_model_data_frame import DataModelDataFrame


class DataModelTabular:
    def __init__(self) -> None:
        self.dict_data_model_data_frame = {}  # This could be an ordered dict but they do not map to json by default

    # index section start
    def __delitem__(self, key) -> None:
        raise NotImplementedError()

    def __getitem__(self, key) -> DataModelDataFrame:
        # TODO check key typing
        return self.get_data_model_data_frame(key)

    def __setitem__(self, key, value):
        raise NotImplementedError()

    # index section end

    # property section start
    @property
    def list_data_frame_name(self) -> List[str]:
        return list(self.dict_data_model_data_frame.keys())

    # property section end

    def get_data_model_data_frame(self, data_frame_name: str) -> DataModelDataFrame:
        if data_frame_name not in self.dict_data_model_data_frame:
            raise Exception(f"No such data_frame_model: {data_frame_name}")
        return self.dict_data_model_data_frame[data_frame_name]

    def add_data_model_data_frame(self, data_model_data_frame: DataModelDataFrame) -> None:
        if data_model_data_frame.data_frame_name in self.dict_data_model_data_frame:
            raise Exception(f"Duplicate data_frame_model: {data_model_data_frame.data_frame_name}")
        self.dict_data_model_data_frame[data_model_data_frame.data_frame_name] = data_model_data_frame

    def to_dict(self) -> Dict:
        dict = {}
        dict["__type__"] = "DataModelTabular"
        dict["dict_data_model_data_frame"] = {}
        for table_id, data_model_data_frame in self.dict_data_model_data_frame.items():
            dict["dict_data_model_data_frame"][table_id] = data_model_data_frame.to_dict()
        import json

        json.dumps(dict)
        return dict

    @staticmethod
    def from_dict(dict: Dict) -> "DataModelTabular":
        data_model_tabular = DataModelTabular()
        for table_id, data_model_data_frame in dict["dict_data_model_data_frame"].items():
            data_model_tabular.dict_data_model_data_frame[table_id] = DataModelDataFrame.from_dict(
                data_model_data_frame
            )

        return data_model_tabular
