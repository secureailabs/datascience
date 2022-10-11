from typing import List

from sail_safe_functions_orchestrator.data_frame_logitudinal import DataFrameLogitudinal
from sail_safe_functions_orchestrator.data_model_logitudinal import DataModelLogitudinal
from sail_safe_functions_orchestrator.data_model_table import DataModelTable


class DataFrameLogitudinalFederated:
    def __init__(self, data_model_logitudinal: DataModelLogitudinal) -> None:
        self._dict_data_frame_logitudinal = {}
        self._data_model_logitudinal = data_model_logitudinal

    def convert_to_table(list_agregator_tabular: DataModelTable):
        raise NotImplementedError()
