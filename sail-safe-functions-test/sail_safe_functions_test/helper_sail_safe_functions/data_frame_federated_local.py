from typing import Dict, List

import numpy as np
import pandas
from pandas import DataFrame as DataFramePandas
from sail_safe_functions_orchestrator.data_frame import DataFrame
from sail_safe_functions_orchestrator.data_frame_federated import DataFrameFederated
from sail_safe_functions_orchestrator.data_model.data_model_data_frame import DataModelDataFrame
from sail_safe_functions_orchestrator.data_model.data_model_series import DataModelSeries
from sail_safe_functions_orchestrator.series_federated import SeriesFederated
from sail_safe_functions_orchestrator.service_reference import ServiceReference
from sail_safe_functions_test.helper_sail_safe_functions.series_federated_local import SeriesFederatedLocal
from sail_safe_functions_test.helper_sail_safe_functions.service_client_local import ServiceClientLocal


class DataFrameFederatedLocal(DataFrameFederated):
    """This should be a multyline docstring"""

    def __init__(self) -> None:
        super().__init__()

    # oveloads
    def create_new(self) -> "DataFrameFederated":
        return DataFrameFederatedLocal()

    # def _get_dataframe_first(self) -> pd.DataFrame:
    #     return list(self.dict_dataframe.values())[0]

    def head(self):
        return self._get_dataframe_first().head()

    @property
    def columns(self):
        return self._get_dataframe_first().columns

    @staticmethod
    def from_csv(dict_csv: Dict[str, str]) -> DataFrameFederated:
        data_model_data_frame = DataModelDataFrame("data_frame_0")
        list_series_name = list(pandas.read_csv(list(dict_csv.values())[0]).columns)
        for series_name in list_series_name:
            data_model_series = DataModelSeries.create_numerical(
                series_name,
                resolution=None,
                measurement_source_name="",
                type_agregator=DataModelSeries.AgregatorCsv,
                unit="unitless",
            )
            data_model_data_frame.add_data_model_series(data_model_series)

        list_reference = []
        for dataset_id, path_file_csv in dict_csv.items():
            data_frame = DataFrame.from_csv(dataset_id, "data_frame_0", data_model_data_frame, path_file_csv)
            list_reference.append(ServiceReference.get_instance().data_frame_to_reference(data_frame))
        # TODO add this again in some way
        # if 0 < len(self.dict_dataframe):
        #     dataframe_first = list(self.dict_dataframe.values())[0]
        #     if set(dataframe_first.columns) != set(dataframe_new.columns):
        #         raise RuntimeError("Dataframe has different columns: " + path_file_csv)
        #         #
        #         # #TODO also check datatype
        #         #
        service_client = ServiceClientLocal()
        return DataFrameFederated(service_client, list_reference, data_model_data_frame)

    def query(self, querystring: str) -> "DataFrameFederatedLocal":
        dataframe_new = DataFrameFederatedLocal()
        for key, dataframe in self.dict_dataframe.items():
            dataframe_new.dict_dataframe[key] = dataframe.query(querystring)

    def to_list_numpy(self) -> List[np.ndarray]:
        list_array_numpy = []
        for dataframe in self.dict_dataframe.values():
            dataframe.to_numpy()
        return list_array_numpy

    # index section

    def __delitem__(self, key) -> None:
        for dataframe in self.dict_dataframe.values():
            dataframe.self.__delitem__(key)

    def __getitem__(self, key) -> "SeriesFederated":
        series = SeriesFederatedLocal()
        for dataframe_key, dataframe in self.dict_dataframe.items():
            series.add_series(dataframe_key, dataframe.__getitem__(key))
        return series

    def __setitem__(self, key, value):
        raise NotImplementedError()

    def to_numpy(self) -> np.ndarray:

        list_array_numpy = []
        for data_frame in self.dict_dataframe.values():
            list_array_numpy.append(data_frame.to_numpy())
        return np.concatenate(list_array_numpy)

    @staticmethod
    def from_numpy(dataset_id, array: np.ndarray, list_name_column=None) -> np.ndarray:
        data_frame = pd.DataFrame(array)
        if list_name_column is not None:
            for name_column_source, name_column_target in zip(data_frame.columns, list_name_column):
                data_frame.rename(columns={name_column_source: name_column_target}, inplace=True)
        data_frame_federated = DataFrameFederatedLocal()
        data_frame_federated.dict_dataframe[dataset_id] = data_frame
        return data_frame_federated
