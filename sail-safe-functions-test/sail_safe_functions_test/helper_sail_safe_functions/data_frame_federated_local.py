from typing import Dict, List

import numpy
import pandas as pd
from sail_safe_functions_orchestrator.data_frame_federated import DataFrameFederated
from sail_safe_functions_orchestrator.series_federated import SeriesFederated
from sail_safe_functions_test.helper_sail_safe_functions.series_federated_local import SeriesFederatedLocal


class DataFrameFederatedLocal(DataFrameFederated):
    """This should be a multyline docstring"""

    def __init__(self) -> None:
        super().__init__()
        self._size = 0

    # oveloads
    def create_new(self) -> "DataFrameFederated":
        return DataFrameFederatedLocal()

    def _get_dataframe_first(self) -> pd.DataFrame:
        return list(self.dict_dataframe.values())[0]

    def head(self):
        return self._get_dataframe_first().head()

    @property
    def size(self) -> int:
        # TODO track this
        size = 0
        for data_frame in self.dict_dataframe.values():
            size += data_frame.shape[0]
        return size

    @property
    def columns(self):
        return self._get_dataframe_first().columns

    def add_csv(self, path_file_csv: str) -> None:
        if path_file_csv in self.dict_dataframe:
            raise RuntimeError("Dataframe alreaddy present: " + path_file_csv)
        dataframe_new = pd.read_csv(path_file_csv)
        if 0 < len(self.dict_dataframe):
            dataframe_first = list(self.dict_dataframe.values())[0]
            if set(dataframe_first.columns) != set(dataframe_new.columns):
                raise RuntimeError("Dataframe has different columns: " + path_file_csv)
                #
                # #TODO also check datatype
                #
        self.dict_dataframe[path_file_csv] = dataframe_new

    def add_data_frame(self, id_dataset, data_frame: pd.DataFrame) -> None:
        self.dict_dataframe[id_dataset] = data_frame

    def query(self, querystring: str) -> "DataFrameFederatedLocal":
        dataframe_new = DataFrameFederatedLocal()
        for key, dataframe in self.dict_dataframe.items():
            dataframe_new.dict_dataframe[key] = dataframe.query(querystring)

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

    def to_list_numpy(self) -> List[numpy.ndarray]:
        list_array_numpy = []
        for dataframe in self.dict_dataframe.values():
            dataframe.to_numpy()
        return list_array_numpy

    def to_numpy(self) -> numpy.ndarray:
        list_array_numpy = []
        for data_frame in self.dict_dataframe.values():
            list_array_numpy.append(data_frame.to_numpy())
        return numpy.concatenate(list_array_numpy)

    def to_numpy_float64(self) -> numpy.ndarray:
        return self.to_numpy().astype(numpy.float64)

    def to_pandas(self) -> pd.DataFrame:
        return pd.concat(list(self.dict_dataframe.values()))

    @staticmethod
    def from_numpy(dataset_id: str, array: numpy.ndarray, list_name_column=None) -> "DataFrameFederated":
        data_frame = pd.DataFrame(array)
        if list_name_column is not None:
            for name_column_source, name_column_target in zip(data_frame.columns, list_name_column):
                data_frame.rename(columns={name_column_source: name_column_target}, inplace=True)
        return DataFrameFederatedLocal.from_data_frame(dataset_id, data_frame)

    @staticmethod
    def from_data_frame(data_frame: pd.DataFrame, count_split=1) -> "DataFrameFederated":
        size_split = int(data_frame.shape[0] / count_split)
        if size_split == 0:
            size_split = 1
        if size_split == 1:
            count_split = data_frame.shape[0]

        index_from = 0
        index_to = 0
        dict_data_frame = {}
        for i in range(count_split):
            index_from = index_to
            index_to = index_from + size_split
            dict_data_frame[f"data_set_id_{str(i)}"] = data_frame.iloc[index_from:index_to, :]
        return DataFrameFederatedLocal.from_dict_data_frame(dict_data_frame)

    @staticmethod
    def from_dict_data_frame(dict_data_frame: Dict[str, pd.DataFrame]) -> "DataFrameFederated":
        data_frame_federated = DataFrameFederatedLocal()
        for dataset_id, data_frame in dict_data_frame.items():
            data_frame_federated.dict_dataframe[dataset_id] = data_frame
        return data_frame_federated

    def print(self):
        for dataset_id, data_frame in self.dict_dataframe.items():
            print(dataset_id)
            print(data_frame.head())
