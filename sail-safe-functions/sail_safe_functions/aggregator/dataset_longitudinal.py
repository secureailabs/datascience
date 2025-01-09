from typing import Dict, List

from sail_safe_functions.aggregator.data_frame import DataFrame
from sail_safe_functions.aggregator.data_model.data_model_data_frame import DataModelDataFrame
from sail_safe_functions.aggregator.data_model.data_model_longitudinal import DataModelLongitudinal
from sail_safe_functions.aggregator.dataset_base import DatasetBase
from sail_safe_functions.aggregator.dataset_tabular import DatasetTabular
from sail_safe_functions.aggregator.series import Series


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
        self.__data_model = data_model
        self.__list_patient = list_patient.copy()

    # property section start

    @property
    def data_model(self) -> DataModelLongitudinal:
        return self.__data_model

    # property section end

    def convert_to_data_frame(
        self,
        data_model_data_frame: DataModelDataFrame,
    ) -> DataFrame:

        list_series = []
        for series_name in data_model_data_frame.list_series_name:
            data_model_series = data_model_data_frame.get_data_model_series(series_name)
            list_data = []
            for patient in self.__list_patient:
                list_data.append(data_model_series.agregate(patient))
            list_series.append(Series(self.dataset_id, data_model_series, list_data))
        return DataFrame(self.dataset_id, data_model_data_frame.data_frame_name, list_series)

    def compute_statistics(self) -> Dict:
        dict_measurement_statistics = {}
        for patient in self.__list_patient:
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
        print(f"patient count : {len(self.__list_patient)}")
        dict_measurement_statistics = self.compute_statistics()

        for key, value in sorted(
            dict_measurement_statistics.items(),
            key=lambda key_value: key_value[1]["count_atleastone"],
            reverse=True,
        ):
            count = value["count_atleastone"] / len(self.__list_patient)
            print(f"{key} {count}")
