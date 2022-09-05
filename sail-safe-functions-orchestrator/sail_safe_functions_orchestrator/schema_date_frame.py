from typing import Dict

from sail_safe_functions_orchestrator.schema_feature import SchemaFeature


# TODO dataclass in python 3.10
class SchemaDataFrame:
    def __init__(self) -> None:
        self.list_name_feature = []
        self.dict_schema_feature = {}  # TODO ordered dict?

    def get_schema_feature(self, feature_name: str) -> SchemaFeature:
        if feature_name not in self.dict_schema_feature:
            raise Exception("No such schema feature")
        return self.dict_schema_feature[feature_name]

    def add_feature_schema(self, schema_feature: SchemaFeature) -> None:
        self.list_name_feature.append(schema_feature.feature_name)
        self.dict_schema_feature[schema_feature.feature_name] = schema_feature.feature_name

    def to_json(self) -> Dict:
        dict_json = {}
        dict_json["list_name_feature"] = self.list_name_feature
        dict_json["dict_schema_feature"] = {}
        for name_feature in self.dict_schema_feature:
            dict_json["dict_schema_feature"][name_feature] = self.get_schema_feature(name_feature).to_json()
        return dict_json

    @staticmethod
    def from_json(dict_json: Dict):
        schema_data_frame = SchemaDataFrame()
        schema_data_frame.list_name_feature = dict_json["list_name_feature"]
        for name_feature in dict_json["dict_schema_feature"]:
            schema_data_frame.dict_schema_feature[name_feature] = SchemaFeature.from_json(
                dict_json["dict_schema_feature"][name_feature]
            )
        return schema_data_frame
