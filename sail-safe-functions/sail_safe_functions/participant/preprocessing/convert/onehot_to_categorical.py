import numpy
from sail_safe_functions.aggregator.data_frame import DataFrame
from sail_safe_functions.aggregator.data_model.data_model_series import DataModelSeries
from sail_safe_functions.aggregator.series import Series
from sail_safe_functions.safe_function_base import SafeFunctionBase


class OnehotToCategorical(SafeFunctionBase):
    @staticmethod
    def run(data_frame_source: DataFrame, data_model_series: DataModelSeries) -> Series:
        if data_model_series.type_data_level != DataModelSeries.DataLevelCategorical:
            raise ValueError()
        series_name = data_model_series.series_name

        list_name_column_selection = []
        for value in data_model_series.list_value:
            list_name_column_selection.append(series_name + "_" + value)

        list_name_column_selection.append(series_name + "_nan")

        data_frame_selection = data_frame_source.select_series(list_name_column_selection)
        series_pandas = data_frame_selection.idxmax(axis=1)  # select the larges column name as value name
        series_pandas = series_pandas.str.slice(start=len(series_name) + 1)  # take away the prefixes
        series_pandas = series_pandas.replace("nan", numpy.nan)
        series = Series.from_pandas(data_frame_source.dataset_id, data_model_series, series_pandas)
        series.index = series_pandas.index
        return series
