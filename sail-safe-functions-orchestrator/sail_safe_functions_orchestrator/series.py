from typing import List

from pandas import Series as SeriesPandas

from sail_safe_functions_orchestrator.data_model.data_model_series import DataModelSeries


class Series(SeriesPandas):
    # NOTE Long term this overloading trick is not maintainable and we will need to create a
    # class where the pandas object in a member not a superclass
    def __init__(self, dataset_id: str, data_model_series: DataModelSeries, list_data: List) -> None:
        super().__init__(data=list_data, name=data_model_series.series_name)
        self.dataset_id = dataset_id
        self.data_model_series = data_model_series

    @property
    def series_name(self):
        return self.data_model_series.series_name

    @staticmethod
    def from_pandas(
        dataset_id: str,
        data_model_series: DataModelSeries,
        series_pandas: SeriesPandas,
    ) -> "Series":
        series = Series(dataset_id, data_model_series, series_pandas.to_list())
        series.index = series_pandas.index
        return series

    # TODO check what feature we use on the Pandas sereies that return pandas series, those will need overloading
