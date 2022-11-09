from typing import Dict, List

from sail_safe_functions_orchestrator.data_model.data_model_series import DataModelSeries


class DataModelDataFrame:
    def __init__(self, data_frame_name) -> None:
        self.data_frame_name = data_frame_name
        self.dict_data_model_series = {}  # This could be an ordered dict but they do not map to json by default

    # index section start
    def __delitem__(self, key) -> None:
        raise NotImplementedError()

    def __getitem__(self, key) -> DataModelSeries:
        # TODO check key typing
        return self.get_data_model_series(key)

    def __setitem__(self, key, value):
        raise NotImplementedError()

    # index section end

    # property section start
    @property
    def list_series_name(self) -> List[str]:
        return list(self.dict_data_model_series.keys())

    # property section end

    def get_data_model_series(self, series_name: str) -> DataModelSeries:
        if series_name not in self.dict_data_model_series:
            raise Exception(f"No such series: {series_name}")
        return self.dict_data_model_series[series_name]

    def add_data_model_series(self, data_model_series: DataModelSeries) -> None:
        if data_model_series.series_name in self.dict_data_model_series:
            raise Exception(f"Duplicate series: {data_model_series.series_name}")
        self.dict_data_model_series[data_model_series.series_name] = data_model_series

    def to_json(self) -> Dict:
        dict_json = {}
        dict_json["data_frame_name"] = self.data_frame_name
        dict_json["dict_data_model_series"] = {}
        for name_feature in self.dict_data_model_series:
            dict_json["dict_data_model_series"][name_feature] = self.get_data_model_series(name_feature).to_json()
        return dict_json

    @staticmethod
    def from_json(dict_json: Dict) -> "DataModelDataFrame":
        data_model_tabular = DataModelDataFrame(dict_json["data_frame_name"])
        for name_feature in dict_json["dict_data_model_series"]:
            data_model_tabular.dict_data_model_series[name_feature] = DataModelSeries.from_json(
                dict_json["dict_data_model_series"][name_feature]
            )
        return data_model_tabular
