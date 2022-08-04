from typing import List

import numpy as np
import pandas as pd
from sail_safe_functions_orchestrator.data_frame_federated import DataFrameFederated
from sail_safe_functions_orchestrator.series_federated import SeriesFederated
from sail_safe_functions_test.helper_sail_safe_functions.series_federated_local import SeriesFederatedLocal


class DataFrameFederatedLocal(DataFrameFederated):
    """This should be a multyline docstring"""

    def __init__(self) -> None:
        super().__init__()

    # oveloads
    def create_new(self) -> "DataFrameFederated":
        return DataFrameFederatedLocal()

    def _get_dataframe_first(self) -> pd.DataFrame:
        return list(self.dict_dataframe.values())[0]

    def head(self):
        return self._get_dataframe_first().head()

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
