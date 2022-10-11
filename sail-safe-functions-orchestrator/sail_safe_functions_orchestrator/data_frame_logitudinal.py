from typing import Dict, List

import pandas

from sail_safe_functions_orchestrator.data_model_table import DataModelTable


class DataFrameLogitudinal:
    def __init__(self, list_patient: List) -> None:
        self.list_patient = list_patient.copy()

    def convert_to_data_frame_table(self, data_model_table: DataModelTable) -> pandas.DataFrame:
        # 4. convert mesurements to table
        dict_feature = {}
        for name_feature in data_model_table.dict_data_model_feature:
            dict_feature[name_feature] = []

        for patient in self.list_patient:
            self.compile_columns(dict_feature, data_model_table, patient)

        data_frame = pandas.DataFrame()
        for name_feature in data_model_table.dict_data_model_feature:
            data_frame[name_feature] = pandas.Series(data=dict_feature[name_feature], name=name_feature)

        return data_frame

    def compile_columns(self, dict_series: Dict[str, List], data_model_table: DataModelTable, patient):
        for feature_name, data_model_feature in data_model_table.dict_data_model_feature.items():
            feature_value = data_model_feature.agregate(patient)
            dict_series[feature_name].append(feature_value)

    def compute_statistics(self) -> Dict:
        dict_measurement_statistics = {}
        for patient in self.list_patient:
            for measurement in patient["dict_measurement"]:
                if measurement not in dict_measurement_statistics:
                    dict_measurement_statistics[measurement] = {}
                    dict_measurement_statistics[measurement]["count_atleastone"] = 0
                    dict_measurement_statistics[measurement]["count_total"] = 0
                    dict_measurement_statistics[measurement]["list_count"] = []
                    dict_measurement_statistics[measurement]["gini"] = 0  # TODO

                dict_measurement_statistics[measurement]["count_atleastone"] += 1
                dict_measurement_statistics[measurement]["count_total"] += len(patient["dict_measurement"][measurement])
                dict_measurement_statistics[measurement]["list_count"].append(
                    len(patient["dict_measurement"][measurement])
                )
        return dict_measurement_statistics

    def print_at_least_one(self) -> None:
        print(f"patient count : {len(self.list_patient)}")
        dict_measurement_statistics = self.compute_statistics()

        for key, value in sorted(
            dict_measurement_statistics.items(),
            key=lambda key_value: key_value[1]["count_atleastone"],
            reverse=True,
        ):
            count = value["count_atleastone"] / len(self.list_patient)
            print(f"{key} {count}")
