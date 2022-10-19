from typing import Dict

from sail_safe_functions_orchestrator.data_model_tabular import \
    DataModelTabular
from sail_safe_functions_orchestrator.dataset_longitudinal import \
    DatasetLongitudinal


class SerializerDatasetBase:
    def __init__(self, dataset_packaging_format) -> None:
        self.dataset_packaging_format = dataset_packaging_format
