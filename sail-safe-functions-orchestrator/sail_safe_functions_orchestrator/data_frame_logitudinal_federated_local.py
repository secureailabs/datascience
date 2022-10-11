from typing import List

from sail_safe_functions_orchestrator.data_frame_logitudinal import DataFrameLogitudinal
from sail_safe_functions_orchestrator.data_frame_logitudinal_federated import DataFrameLogitudinalFederated
from sail_safe_functions_orchestrator.data_model_logitudinal import DataModelLogitudinal
from sail_safe_functions_orchestrator.data_model_table import DataModelTable


class DataFrameLogitudinalFederatedLocal(DataFrameLogitudinalFederated):
    def __init__(self, data_model_logitudinal: DataModelLogitudinal) -> None:
        super().__init__(data_model_logitudinal)

    def add_data_frame_logitudinal(self, id_dataset: str, data_frame_longitudinal: DataFrameLogitudinal):
        self._dict_data_frame_logitudinal[id_dataset] = data_frame_longitudinal

    def convert_to_table(list_agregator_tabular: DataModelTable):
        raise NotImplementedError()
