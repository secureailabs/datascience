from typing import Dict

from sail_safe_functions_orchestrator.data_model_feature import DataModelFeature


class DataModelTable:
    def __init__(self) -> None:
        self.list_name_feature = []
        self.dict_data_model_feature = {}  # This could be an ordered dict but they do not map to json by default

    def get_data_model_feature(self, feature_name: str) -> DataModelFeature:
        if feature_name not in self.dict_data_model_feature:
            raise Exception("No such feature")
        return self.dict_data_model_feature[feature_name]

    def add_data_model_feature(self, data_model_feature: DataModelFeature) -> None:
        self.list_name_feature.append(data_model_feature.feature_name)
        self.dict_data_model_feature[data_model_feature.feature_name] = data_model_feature

    def to_json(self) -> Dict:
        dict_json = {}
        dict_json["list_name_feature"] = self.list_name_feature
        dict_json["dict_data_model_feature"] = {}
        for name_feature in self.dict_data_model_feature:
            dict_json["dict_data_model_feature"][name_feature] = self.get_data_model_feature(name_feature).to_json()
        return dict_json

    @staticmethod
    def from_json(dict_json: Dict):
        data_model_table = DataModelTable()
        data_model_table.list_name_feature = dict_json["list_name_feature"]
        for name_feature in dict_json["dict_data_model_feature"]:
            data_model_table.dict_data_model_feature[name_feature] = DataModelFeature.from_json(
                dict_json["dict_data_model_feature"][name_feature]
            )
        return data_model_table
