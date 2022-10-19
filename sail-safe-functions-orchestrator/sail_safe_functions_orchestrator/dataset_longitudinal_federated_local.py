from typing import List

from sail_safe_functions_orchestrator.data_model_longitudinal import DataModelLongitudinal
from sail_safe_functions_orchestrator.data_model_tabular import DataModelTabular
from sail_safe_functions_orchestrator.dataset_longitudinal import DatasetLongitudinal
from sail_safe_functions_orchestrator.dataset_longitudinal_federated import DatasetLongitudinalFederated


class DatasetLongitudinalFederatedLocal(DatasetLongitudinalFederated):
    def __init__(self, data_model_longitudinal: DataModelLongitudinal) -> None:
        super().__init__(data_model_longitudinal)

    def add_data_frame_longitudinal(self, id_dataset: str, data_frame_longitudinal: DatasetLongitudinal):
        self._dict_data_frame_longitudinal[id_dataset] = data_frame_longitudinal

    def convert_to_table(list_agregator_tabular: DataModelTabular):
        raise NotImplementedError()
