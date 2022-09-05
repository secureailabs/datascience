from typing import Dict, List


class SchemaFeature:
    DataLevelUnique = "DataLevelUnique"
    DataLevelCategorical = "DataLevelCategorical"
    DataLevelInterval = "DataLevelInterval"

    MissingPolicyPropagateAddColumn = "MissingPolicyPropagateAddColumn"
    MissingPolicyRaiseException = "MissingPolicyRaiseException"

    def __init__(
        self, feature_name: str, data_level: str, missing_policy: str, resolution: float, list_value: List[str]
    ) -> None:
        if data_level not in [
            SchemaFeature.DataLevelUnique,
            SchemaFeature.DataLevelCategorical,
            SchemaFeature.DataLevelInterval,
        ]:
            raise ValueError(f"Illegal value data_level: {data_level}")
        if missing_policy not in [
            SchemaFeature.MissingPolicyPropagateAddColumn,
            SchemaFeature.MissingPolicyRaiseException,
        ]:
            raise ValueError(f"Illegal value missing_policy: {missing_policy}")
        if data_level == SchemaFeature.DataLevelCategorical:
            if list_value is None:
                raise ValueError(f"list_value cannot be None")
            if len(list_value) == 0:
                raise ValueError(f"list_value must be at least size 1")
            if len(list_value) != len(set(list_value)):
                raise ValueError(f"list_value can only contain unique values")

        self.feature_name = feature_name
        self.data_level = data_level
        self.missing_policy = missing_policy
        self.resolution = resolution  # for numerical
        self.list_value = list_value  # for cathegorical

    def create_unique(feature_name: str):
        return SchemaFeature(
            feature_name,
            SchemaFeature.DataLevelUnique,
            None,
            None,
            None,
        )

    def create_numerical(feature_name: str, missing_policy: str, resolution: float):
        return SchemaFeature(
            feature_name,
            SchemaFeature.DataLevelInterval,
            missing_policy,
            resolution,
            None,
        )

    def create_cathegorical(feature_name: str, missing_policy: str, resolution: float):
        return SchemaFeature(
            feature_name,
            SchemaFeature.DataLevelInterval,
            missing_policy,
            resolution,
            None,
        )

    def to_json(self) -> Dict:
        dict_json = {}
        dict_json["feature_name"] = self.feature_name
        dict_json["data_level"] = self.data_level
        dict_json["missing_policy"] = self.missing_policy
        dict_json["resolution"] = self.resolution
        dict_json["list_value"] = self.list_value
        return dict_json

    def from_json(dict_json: Dict) -> "SchemaFeature":
        return SchemaFeature(
            dict_json["feature_name"],
            dict_json["data_level"],
            dict_json["missing_policy"],
            dict_json["resolution"],
            dict_json["list_value"],
        )
