from typing import List

import numpy as np
import pandas as pd
from sail_safe_functions_orchestrator.dataframe_federated import DataframeFederated
from sail_safe_functions_orchestrator.series_federated import SeriesFederated
from sail_safe_functions_test.helper_sail_safe_functions.series_federated_local import SeriesFederatedLocal


class DataframeFederatedLocal(DataframeFederated):
    """This should be a multyline docstring"""

    def __init__(self) -> None:
        self.dict_dataframe = {}

    def _get_dataframe_first(self) -> pd.DataFrame:
        return list(self.dict_dataframe.values())[0]

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

    def query(self, querystring: str) -> "DataframeFederatedLocal":
        dataframe_new = DataframeFederatedLocal()
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
