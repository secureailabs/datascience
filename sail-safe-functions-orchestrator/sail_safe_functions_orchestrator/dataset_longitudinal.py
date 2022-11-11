from typing import Dict, List

from sail_safe_functions_orchestrator.data_frame import DataFrame
from sail_safe_functions_orchestrator.data_model.data_model_longitudinal import DataModelLongitudinal
from sail_safe_functions_orchestrator.data_model.data_model_tabular import DataModelTabular
from sail_safe_functions_orchestrator.dataset_base import DatasetBase
from sail_safe_functions_orchestrator.dataset_tabular import DatasetTabular
from sail_safe_functions_orchestrator.series import Series


class DatasetLongitudinal(DatasetBase):
    def __init__(
        self,
        dataset_federation_id: str,
        dataset_federation_name: str,
        dataset_id: str,
        dataset_name: str,
        data_model: DataModelLongitudinal,
        list_patient: List,
    ) -> None:
        super().__init__(dataset_federation_id, dataset_federation_name, dataset_id, dataset_name)
        self.data_model = data_model
        self.list_patient = list_patient.copy()

    def convert_to_dataset_tabular(
        self,
        dataset_federation_id: str,
        dataset_federation_name: str,
        dataset_id: str,
        dataset_name: str,
        data_model_tabular: DataModelTabular,
    ) -> DatasetTabular:
        list_data_frame = []
        for data_frame_name in data_model_tabular.list_data_frame_name:
            data_model_data_frame = data_model_tabular.get_data_model_data_frame(data_frame_name)
            list_series = []
            for series_name in data_model_data_frame.list_series_name:
                data_model_series = data_model_data_frame.get_data_model_series(series_name)
                list_data = []
                for patient in self.list_patient:
                    list_data.append(data_model_series.agregate(patient))
                list_series.append(Series(dataset_id, data_model_series, list_data))

            list_data_frame.append(DataFrame(dataset_id, data_frame_name, list_series))

        return DatasetTabular(dataset_federation_id, dataset_federation_name, dataset_id, dataset_name, list_data_frame)

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
