import random
from typing import Dict, List, Optional, Tuple

import numpy as np
import pandas
from pandas.api.types import is_numeric_dtype, is_string_dtype
from sail_safe_functions.aggregator import statistics
from sail_safe_functions.aggregator.data_frame import DataFrame
from sail_safe_functions.aggregator.data_frame_federated import DataFrameFederated
from sail_safe_functions.aggregator.data_model.data_model_data_frame import DataModelDataFrame
from sail_safe_functions.aggregator.data_model.data_model_series import DataModelSeries
from sail_safe_functions.aggregator.dataset_longitudinal_federated import DatasetLongitudinalFederated
from sail_safe_functions.aggregator.packager_dataset.packager_data_federation import PackagerDataFederation
from sail_safe_functions.aggregator.packager_dataset.serializer_dataset_fhirv1 import SerializerDatasetFhirv1
from sail_safe_functions.aggregator.series import Series
from sail_safe_functions.aggregator.series_federated import SeriesFederated
from sail_safe_functions.aggregator.service_reference import ServiceReference


def series_drop_by_index(series_federated: SeriesFederated, index_drop: int):
    # TODO write a unit test for this
    list_reference = []
    service_reference = ServiceReference.get_instance()
    for dataset_id in series_federated.list_dataset_id:
        series: Series = service_reference.reference_to_series(series_federated.get_reference_series(dataset_id))
        if 0 < index_drop and index_drop < series.size:
            series_pandas = series.drop(index_drop)
        else:
            series_pandas = series
        Series.from_pandas(dataset_id, series.data_model_series, series_pandas)
        list_reference.append(service_reference.series_to_reference(series))
    return SeriesFederated(list_reference, series_federated.data_model_series)


def series_split_random(
    series_federated: SeriesFederated, sample_size_0: int, random_seed: Optional[int] = None
) -> Tuple[SeriesFederated, SeriesFederated]:
    # TODO write a unit test for this
    series_federated_size = statistics.count(series_federated)
    if series_federated_size < sample_size_0:
        raise Exception("sample_size_0 too large")

    list_index = list(range(series_federated_size))
    if random_seed is not None:
        random.seed(random_seed)
    random.shuffle(list_index)
    array_index_0 = np.array(sorted(list_index[sample_size_0:]))
    array_index_1 = np.array(sorted(list_index[:sample_size_0]))
    service_reference = ServiceReference.get_instance()
    list_reference_0 = []
    list_reference_1 = []

    for dataset_id in series_federated.list_dataset_id:
        series: Series = service_reference.reference_to_series(series_federated.get_reference_series(dataset_id))
        series_size = series.size
        array_index_0_series = array_index_0[0 <= array_index_0 & array_index_0 < series_size]
        array_index_1_series = array_index_1[0 <= array_index_0 & array_index_0 < series_size]
        array_index_0 = array_index_0 - series_size
        array_index_1 = array_index_1 - series_size
        series_pandas_0 = series.take(array_index_0_series)
        series_pandas_1 = series.take(array_index_1_series)
        series_0 = Series.from_pandas(dataset_id, series.data_model_series, series_pandas_0)
        series_1 = Series.from_pandas(dataset_id, series.data_model_series, series_pandas_1)
        list_reference_0.append(service_reference.series_to_reference(series_0))
        list_reference_1.append(service_reference.series_to_reference(series_1))
    series_federated_0 = SeriesFederated(list_reference_0, series_federated.data_model_series)
    series_federated_1 = SeriesFederated(list_reference_1, series_federated.data_model_series)
    return series_federated_0, series_federated_1


class ToolsDataTest:
    """Tools to interact with federated data"""

    # @staticmethod
    # def from_numpy(dataset_id, array: np.ndarray, list_name_column=None) -> np.ndarray:
    #     data_frame = pandas.DataFrame(array)
    #     if list_name_column is not None:
    #         for name_column_source, name_column_target in zip(data_frame.columns, list_name_column):
    #             data_frame.rename(columns={name_column_source: name_column_target}, inplace=True)
    #     data_frame_federated = DataFrameFederatedLocal()
    #     data_frame_federated.dict_dataframe[dataset_id] = data_frame
    #     return data_frame_federated

    @staticmethod
    def from_csv(dict_csv: Dict[str, str]) -> DataFrameFederated:
        data_model_data_frame = DataModelDataFrame("data_frame_0")
        # TODO do this for multy csv as well
        data_frame_pandas = pandas.read_csv(list(dict_csv.values())[0])
        list_series_name = data_frame_pandas.columns
        for series_name in list_series_name:
            if is_numeric_dtype(data_frame_pandas[series_name]):
                data_model_series = DataModelSeries.create_numerical(
                    series_name,
                    resolution=None,
                    measurement_source_name="",
                    type_agregator=DataModelSeries.AgregatorCsv,
                    unit="unitless",
                )

            elif is_string_dtype(data_frame_pandas[series_name]):
                list_value = pandas.unique(data_frame_pandas[series_name])
                if len(list_value) == len(data_frame_pandas[series_name]):
                    data_model_series = DataModelSeries.create_unique(
                        series_name,
                        type_agregator=DataModelSeries.AgregatorCsv,
                    )

                else:
                    data_model_series = DataModelSeries.create_categorical(
                        series_name,
                        list_value,
                        type_agregator=DataModelSeries.AgregatorCsv,
                    )

            else:
                raise ValueError("Neither numeric or string dtype")
            data_model_data_frame.add_data_model_series(data_model_series)
        list_reference = []
        for dataset_id, path_file_csv in dict_csv.items():
            data_frame = DataFrame.from_csv(dataset_id, "data_frame_0", data_model_data_frame, path_file_csv)
            list_reference.append(ServiceReference.get_instance().data_frame_to_reference(data_frame))

        return DataFrameFederated(list_reference, data_model_data_frame)

    @staticmethod
    def from_array(dataset_id, series_name: str, array: np.ndarray) -> SeriesFederated:
        data_model_series = DataModelSeries.create_numerical(
            series_name,
            resolution=None,
            measurement_source_name="",
            type_agregator=DataModelSeries.AgregatorCsv,
            unit="unitless",
        )

        series = Series(dataset_id, data_model_series, array.tolist())
        list_reference = [ServiceReference.get_instance().series_to_reference(series)]

        return SeriesFederated(list_reference, data_model_series)

    @staticmethod
    def from_dict_array(series_name: str, dict_array: Dict[str, np.ndarray]) -> SeriesFederated:
        data_model_series = DataModelSeries.create_numerical(
            series_name,
            resolution=None,
            measurement_source_name="",
            type_agregator=DataModelSeries.AgregatorCsv,
            unit="unitless",
        )

        list_reference = []
        for dataset_id, array in dict_array.items():
            series = Series(dataset_id, data_model_series, array.tolist())
            list_reference.append(ServiceReference.get_instance().series_to_reference(series))
        return SeriesFederated(list_reference, data_model_series)

    @staticmethod
    def read_for_path_file(path_file_data_federation: str) -> DatasetLongitudinalFederated:
        # TODO call safe function via RPC ReadDatasetFhirv1Precompute
        packager = PackagerDataFederation()
        packager.prepare_data_federation(path_file_data_federation)
        dict_dataset_name_to_dataset_id = packager.get_dict_dataset_name_to_dataset_id(path_file_data_federation)
        data_model_longitudinal = {}
        serializer = SerializerDatasetFhirv1()
        list_reference = []
        for dataset_id in dict_dataset_name_to_dataset_id.values():
            dataset_longitudinal = serializer.read_dataset(dataset_id)
            list_reference.append(
                ServiceReference.get_instance().dataset_longitudinal_to_reference(dataset_longitudinal)
            )

        return DatasetLongitudinalFederated(list_reference, data_model_longitudinal)
