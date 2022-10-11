import json
import statistics
from typing import Dict, List


class DataModelFeature:
    DataLevelUnique = "DataLevelUnique"
    DataLevelCategorical = "DataLevelCategorical"
    DataLevelInterval = "DataLevelInterval"

    MissingPolicyPropagateAddColumn = "MissingPolicyPropagateAddColumn"
    MissingPolicyRaiseException = "MissingPolicyRaiseException"

    AgregatorCsv = "AgregatorCsv"
    AgregatorPatientGender = "AgregatorPatientGender"
    AgregatorPatientMaritalStatus = "AgregatorPatientMaritalStatus"
    AgregatorPatientRace = "AgregatorPatientRace"
    AgregatorPatientEthnicity = "AgregatorPatientEthnicity"
    AgregatorIntervalFirstOccurance = "AgregatorIntervalFirstOccurance"
    AgregatorIntervalLastOccurance = "AgregatorIntervalLastOccurance"
    AgregatorIntervalCountOccurance = "AgregatorIntervalCountOccurance"
    AgregatorIntervalMean = "AgregatorIntervalMean"
    AgregatorCategoricalFirstOccurance = "AgregatorCategoricalFirstOccurance"
    AgregatorCategoricalLastOccurance = "AgregatorCategoricalLastOccurance"
    AgregatorCategoricalCountOccurance = "AgregatorCategoricalCountOccurance"
    AgregatorCategoricalMostFrequent = "AgregatorCategoricalMostFrequent"

    def __init__(
        self,
        feature_name: str,
        type_data_level: str,
        resolution: float,
        list_value: List[str],
        measurement_source_name: str = None,
        type_agregator: str = None,
    ) -> None:
        if type_data_level not in [
            DataModelFeature.DataLevelUnique,
            DataModelFeature.DataLevelCategorical,
            DataModelFeature.DataLevelInterval,
        ]:
            raise ValueError(f"Illegal value data_level: {type_data_level}")

        if type_data_level == DataModelFeature.DataLevelCategorical:
            if list_value is None:
                raise ValueError(f"list_value cannot be None")
            if len(list_value) == 0:
                raise ValueError(f"list_value must be at least size 1")
            if len(list_value) != len(set(list_value)):
                raise ValueError(f"list_value can only contain unique values")

        self.feature_name = feature_name
        self.type_data_level = type_data_level
        self.type_agregator = type_agregator
        self.measurement_source_name = measurement_source_name
        self.unit = ""  # for numerical
        self.value_min = ""  # for numerical
        self.value_max = ""  # for numerical
        self.resolution = resolution  # for numerical

        self.list_value = list_value  # for cathegorical

    def agregate(self, patient):
        try:
            # patient resource lookup
            # TODO refactor this
            if self.type_data_level == DataModelFeature.AgregatorPatientGender:
                return patient["resource"]["gender"]
                # TODO there is also this attribute
                #          {
                #     "url": "http://hl7.org/fhir/us/core/StructureDefinition/us-core-birthsex",
                #     "valueCode": "F"
                # },
            elif self.type_data_level == DataModelFeature.AgregatorPatientMaritalStatus:
                return patient["resource"]["maritalStatus"]["coding"][0]["display"]
            elif self.type_data_level == DataModelFeature.AgregatorPatientRace:
                for extension in patient["resource"]["extension"]:
                    if extension["url"] == "http://hl7.org/fhir/us/core/StructureDefinition/us-core-race":
                        return extension["extension"][0]["valueCoding"]["display"]
                return None
            elif self.type_data_level == DataModelFeature.AgregatorPatientEthnicity:
                for extension in patient["resource"]["extension"]:
                    if extension["url"] == "http://hl7.org/fhir/us/core/StructureDefinition/us-core-ethnicity":
                        return extension["extension"][0]["valueCoding"]["display"]
                return None

            elif self.type_data_level == DataModelFeature.DataLevelInterval:
                # TODO also enforce resolution, and add that to the schema
                if self.measurement_source_name not in patient["dict_measurement"]:
                    if self.type_agregator == DataModelFeature.AgregatorIntervalCountOccurance:
                        return 0
                    else:
                        return None

                list_measurement = patient["dict_measurement"][self.measurement_source_name]
                if self.type_agregator == DataModelFeature.AgregatorIntervalFirstOccurance:
                    return list_measurement[0]["event_value"]
                if self.type_agregator == DataModelFeature.AgregatorIntervalLastOccurance:
                    return list_measurement[-1]["event_value"]
                if self.type_agregator == DataModelFeature.AgregatorIntervalCountOccurance:
                    return len(list_measurement)
                if self.type_agregator == DataModelFeature.AgregatorIntervalMean:
                    list_measurement_value = [measurement["event_value"] for measurement in list_measurement]
                    return statistics.mean(list_measurement_value)

                else:
                    raise Exception(f"unkown type_agregator {self.type_agregator}")

            elif self.type_data_level == DataModelFeature.DataLevelCategorical:
                if self.measurement_source_name not in patient["dict_measurement"]:
                    if self.type_agregator == DataModelFeature.AgregatorCategoricalCountOccurance:
                        return 0
                    else:
                        return None

                list_measurement = patient["dict_measurement"][self.measurement_source_name]
                if self.type_agregator == DataModelFeature.AgregatorCategoricalFirstOccurance:
                    return list_measurement[0]["event_value"]
                if self.type_agregator == DataModelFeature.AgregatorCategoricalLastOccurance:
                    return list_measurement[-1]["event_value"]
                if self.type_agregator == DataModelFeature.AgregatorCategoricalCountOccurance:
                    return len(list_measurement)
                if self.type_agregator == DataModelFeature.AgregatorCategoricalMostFrequent:
                    raise NotImplementedError()  # TODO implement
                else:
                    raise Exception(f"unkown type_agregator {self.type_agregator}")

            else:
                raise Exception(f"unkown type_feature {self.type_data_level}")

        except Exception as exception:
            print(json.dumps(patient["resource"], indent=4, sort_keys=True))
            raise exception
        raise Exception(f"cannot return default")

    def create_unique(feature_name: str) -> "DataModelFeature":
        return DataModelFeature(feature_name, DataModelFeature.DataLevelUnique, None, None, None, None)

    def create_numerical(
        feature_name: str, resolution: float = -1, measurement_source_name: str = None, type_agregator: str = None
    ) -> "DataModelFeature":
        return DataModelFeature(
            feature_name, DataModelFeature.DataLevelInterval, resolution, None, measurement_source_name, type_agregator
        )

    def create_categorical(
        feature_name: str, list_value: List[str], measurement_source_name: str = None, type_agregator: str = None
    ) -> "DataModelFeature":
        return DataModelFeature(
            feature_name, DataModelFeature.DataLevelInterval, None, list_value, measurement_source_name, type_agregator
        )

    def to_json(self) -> Dict:
        dict_json = {}
        dict_json["feature_name"] = self.feature_name
        dict_json["type_agregator"] = self.type_data_level
        dict_json["resolution"] = self.resolution
        dict_json["list_value"] = self.list_value
        dict_json["measurement_source_name"] = self.measurement_source_name
        dict_json["type_agregator"] = self.type_agregator
        return dict_json

    def from_json(dict_json: Dict) -> "DataModelFeature":
        return DataModelFeature(
            dict_json["feature_name"],
            dict_json["type_agregator"],
            dict_json["resolution"],
            dict_json["list_value"],
            dict_json["measurement_source_name"],
            dict_json["type_agregator"],
        )
