from io import BytesIO, StringIO
from typing import List

import pandas
from pandas import DataFrame as DataFramePandas

from sail_safe_functions_orchestrator.data_model.data_model_data_frame import DataModelDataFrame
from sail_safe_functions_orchestrator.series import Series


class DataFrame(DataFramePandas):
    # NOTE Long term this overloading trick is not maintainable and we will need to create a
    # class where the pandas object in a member not a superclass

    def __init__(self, dataset_id: str, data_frame_name: str, list_series: List[Series]) -> None:
        super().__init__()
        self.dataset_id = dataset_id
        self.data_frame_name = data_frame_name
        self.data_model_data_frame = DataModelDataFrame(data_frame_name)
        for series in list_series:
            self.add_series(series)

    def get_series(self, series_name: str) -> Series:
        if series_name not in self.list_series_name:
            raise Exception(f"No such series: {series_name}")
        return Series(
            self.dataset_id,
            series_name,
            self.data_model_data_frame[series_name],
            super().__getitem__(series_name).to_list(),
        )

    def add_series(self, series: Series):
        if series.series_name in self.columns:
            raise ValueError(f"Duplicate series: {series.series_name}")
        # TODO overload this indexer as well !!!!
        super().__setitem__(series.series_name, series)
        self.data_model_data_frame.add_data_model_series(series.data_model_series)

    # index section start
    def __delitem__(self, key) -> None:
        raise NotImplementedError()

    def __getitem__(self, key) -> Series:
        # TODO check key typing
        return self.get_series(key)

    def __setitem__(self, key, value):
        raise NotImplementedError()

    # index section end

    # property section start
    @property
    def list_series_name(self) -> List[str]:
        return list(self.columns)

    # property section end

    def from_csv(
        dataset_id: str, data_frame_name: str, data_model_data_frame: DataModelDataFrame, path_file_csv: str
    ) -> "DataFrame":
        with open(path_file_csv, "rb") as file:
            return DataFrame.from_csv_str(dataset_id, data_frame_name, data_model_data_frame, file.read())

    def from_csv_str(
        dataset_id: str,
        data_frame_name: str,
        data_model_data_frame: DataModelDataFrame,
        csv_content: str,
    ) -> "DataFrame":
        set_series_name = set(data_model_data_frame.list_series_name)  # gutted object
        data_frame_pandas = pandas.read_csv(BytesIO(csv_content))
        list_series = []
        for series_name in data_model_data_frame.list_series_name:
            list_data = data_frame_pandas[series_name].to_list()
            list_series.append(Series(dataset_id, series_name, data_model_data_frame[series_name], list_data))
            set_series_name.remove(series_name)

        if 0 < len(set_series_name):
            raise Exception(f"Missing series: {list(set_series_name)}")
        return DataFrame(dataset_id, data_frame_name, list_series)

    # TODO check what feature we use on the Pandas data_frame that return pandas data_frame or series, those will need overloading
