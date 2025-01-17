from typing import List

import numpy
import pandas
from sail_safe_functions.aggregator.data_model.data_model_series import DataModelSeries
from sail_safe_functions.aggregator.series import Series
from sail_safe_functions.safe_function_base import SafeFunctionBase


class CategoricalToOnehot(SafeFunctionBase):
    @staticmethod
    def run(series: Series) -> List[Series]:
        if series.data_model_series.type_data_level != DataModelSeries.DataLevelCategorical:
            raise ValueError()

        data_frame_pandas = pandas.get_dummies(
            series,
            prefix=series.series_name,
            prefix_sep="_",
            dummy_na=True,
            columns=series.data_model_series.list_value,
            sparse=False,
            drop_first=False,
            dtype=numpy.float64,
        )
        list_series = []
        for series_name in data_frame_pandas.columns:
            series_pandas = data_frame_pandas[series_name]
            data_model_series = DataModelSeries.create_numerical(
                series_name, -1, type_agregator=DataModelSeries.AgregatorComputed
            )
            series_created = Series.from_pandas(series_name, data_model_series, series_pandas)
            series_created.index = series_pandas.index
            list_series.append(series_created)
        return list_series
