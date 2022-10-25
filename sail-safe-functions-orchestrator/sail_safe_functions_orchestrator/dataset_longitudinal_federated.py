from typing import List

from sail_safe_functions_orchestrator.data_model.data_model_longitudinal import DataModelLongitudinal
from sail_safe_functions_orchestrator.data_model.data_model_tabular import DataModelTabular
from sail_safe_functions_orchestrator.dataset_longitudinal import DatasetLongitudinal


class DatasetLongitudinalFederated:
    def __init__(self, data_model_longitudinal: DataModelLongitudinal) -> None:
        self.dict_dataset = {}
        self.data_model_longitudinal = data_model_longitudinal

    def add_dataset(self, dataset: DatasetLongitudinal) -> None:
        self.dict_dataset[dataset.dataset_id] = dataset

    def convert_to_table(list_agregator_tabular: DataModelTabular):
        raise NotImplementedError()
