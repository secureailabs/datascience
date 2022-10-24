from typing import List

from pandas import Series as SeriesPandas

from sail_safe_functions_orchestrator.data_model_series import DataModelSeries


class Series(SeriesPandas):
    # NOTE Long term this overloading trick is not maintainable and we will need to create a
    # class where the pandas object in a member not a superclass
    def __init__(self, series_name: str, data_model_series: DataModelSeries, list_data: List) -> None:
        super().__init__(data=list_data, name=series_name)
        self.series_name = series_name
        self.data_model_series = data_model_series

    # TODO check what feature we use on the Pandas sereies that return pandas series, those will need overloading
