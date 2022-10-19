from typing import Dict

from pandas import DataFrame

from sail_safe_functions_orchestrator.data_model_tabular import DataModelTabular


class DatasetTabular:
    def __init__(self, dataset_id: str, data_model: DataModelTabular, dict_table: Dict[str, DataFrame]) -> None:
        # TODO have the data_model validate the dict_table
        self._dataset_id = dataset_id
        self._data_model = data_model
        self._dict_table = dict_table.copy()
