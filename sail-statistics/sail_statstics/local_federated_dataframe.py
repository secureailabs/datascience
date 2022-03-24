import pandas as pd
import numpy as np
from typing import List

from sail_statstics.federated_dataframe import FederatedDataframe


class LocalFederatedDataframe(FederatedDataframe):
    def __init__(self) -> None:
        super().__init__()
        self.dict_dataframe = {}

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

    def query(self, querystring: str) -> "LocalFederatedDataframe":
        dataframe_new = LocalFederatedDataframe()
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

    def __getitem__(self, key) -> "LocalFederatedDataframe":
        dataframe_new = LocalFederatedDataframe()
        for dataframe_key, dataframe in self.dict_dataframe.items():
            dataframe_new.dict_dataframe[dataframe_key] = dataframe.__getitem__(key)
        return dataframe_new

    def __setitem__(self, key, value):
        raise NotImplementedError()

    def to_numpy(self) -> np.ndarray:
        list_array_numpy = []
        for dataframe in self.dict_dataframe.values():
            list_array_numpy.append(dataframe.to_numpy())
        return np.concatenate(list_array_numpy)
