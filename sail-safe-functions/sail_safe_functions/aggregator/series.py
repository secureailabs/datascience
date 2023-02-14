from typing import List

import numpy as np
from pandas import Series as SeriesPandas
from sail_safe_functions.aggregator.data_model.data_model_series import DataModelSeries


class Series:
    # NOTE Long term this overloading trick is not maintainable and we will need to create a
    # class where the pandas object in a member not a superclass
    # TODO Put the datamodel last because we do that everwhere else
    def __init__(self, dataset_id: str, data_model_series: DataModelSeries, list_data: List) -> None:
        # TODO trying to avoid circular import here solution would be to move the reference but that is invasive
        if not isinstance(dataset_id, str):
            raise Exception(f"{dataset_id} is not instance of class: {str} instead type is {type(dataset_id)}")
        if not isinstance(data_model_series, DataModelSeries):
            raise Exception(
                f"{data_model_series} is not instance of class: {DataModelSeries} instead type is {type(data_model_series)}"
            )
        self._dataset_id = dataset_id
        self._data_model_series = data_model_series
        self.data = list_data
        self.name = data_model_series.series_name
        self.series_pandas = SeriesPandas(data=list_data, name=data_model_series.series_name)
        self.index = SeriesPandas.index
        self.size = SeriesPandas.size

    @property
    def series_name(self) -> str:
        return self._data_model_series.series_name

    def to_numpy(self) -> np.ndarray:
        return self.series_pandas.to_numpy()

    def value_counts(self):
        return self.series_pandas.value_counts()

    def to_list(self):
        return self.series_pandas.to_list()

    @property
    def dataset_id(self) -> str:
        return self._dataset_id

    @property
    def data_model_series(self) -> DataModelSeries:
        return self._data_model_series

    @staticmethod
    def from_pandas(
        dataset_id: str,
        data_model_series: DataModelSeries,
        series_pandas: SeriesPandas,
    ) -> "Series":
        if series_pandas.dtype == int:
            # dtype is aways float no ints allowed at this point
            series_pandas = series_pandas.astype(float)
        series = Series(dataset_id, data_model_series, series_pandas.to_list())
        series.index = series_pandas.index
        return series

    # TODO check what feature we use on the Pandas series that return pandas series, those will need overloading
