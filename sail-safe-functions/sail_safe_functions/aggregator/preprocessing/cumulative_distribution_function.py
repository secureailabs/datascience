from typing import List

from pandas import DataFrame as DataFramePandas


class CumulativeDistributionFunction:
    def __init__(self, list_domain: List, list_data_model_series: List[DataModelSeries]) -> None:
        pass

    def sample_list(self, sample_count: int, enforce_resolution: bool) -> List[List[float]]:
        return

    def sample_data_frame(self, sample_count: int) -> DataFramePandas:
        # TODO change this into some private dataframe that still has models
        list_sample = self.sample_list(sample_count)

        return DataFramePandas()
