from typing import Dict

import numpy as np
import pandas as pd
from pandas.api.types import is_numeric_dtype
from sail_safe_functions_orchestrator.series_federated import SeriesFederated


class SeriesFederatedLocal(SeriesFederated):
    """
    Helper class for testing federated statics, it incorperates several series but pretends to be asingle one
    """

    def __init__(self, name: str = None) -> None:
        super().__init__(name)
        self.dtype = None
        self.is_numeric = None

    @property
    def size(self):
        size = 0
        for series in self._dict_series.values():
            size += series.size
        return size

    def add_series(self, dataset_id: str, series: pd.Series):
        if self.name is None:
            self.name = series.name

        if self.dtype is None:
            self.dtype = series.dtype

        if self.is_numeric is None:
            self.is_numeric = is_numeric_dtype(series)

        else:
            if self.name != series.name:
                raise RuntimeError("Cannot add series with different name")

            if self.dtype != series.dtype:
                raise RuntimeError("Cannot add series with different dtype")

            if self.is_numeric != is_numeric_dtype(series):
                raise RuntimeError("Cannot add series with different is_numeric")
        self.dict_series[dataset_id] = series

    def add_array(self, key: str, array: np.ndarray, name: str = None):
        if name is not None:
            self.add_series(key, pd.Series(data=array, name=self.name))
        else:
            self.add_series(key, pd.Series(data=array, name=name))

    def to_numpy(self) -> np.ndarray:
        list_array_numpy = []
        for series in self.dict_series.values():
            list_array_numpy.append(series.to_numpy())
        return np.concatenate(list_array_numpy)

    def drop_by_index(self, index_to_drop) -> "SeriesFederatedLocal":
        series_federated_new = SeriesFederatedLocal()
        for dataset_id in self.dict_series:
            series = self.dict_series[dataset_id]
            if 0 <= index_to_drop and index_to_drop < series.size:
                series = series.drop(series.index[index_to_drop])
            index_to_drop -= series.size + 1
            series_federated_new.add_series(dataset_id, series)
        return series_federated_new

    def create_new(self) -> "SeriesFederated":
        return SeriesFederatedLocal()

    def to_series(self) -> pd.Series:
        return pd.Series(self.to_numpy(), name=self.name)

    def describe(self) -> Dict:
        dict_discribe = {}
        dict_discribe["name"] = self.name
        dict_discribe["dtype"] = self.dtype
        dict_discribe["is_numeric"] = self.is_numeric
        return dict_discribe

    @staticmethod
    def from_array(name: str, array: np.ndarray) -> pd.Series:
        series = SeriesFederatedLocal(name)
        series.add_array("dataset_0", array, name)
        return series
