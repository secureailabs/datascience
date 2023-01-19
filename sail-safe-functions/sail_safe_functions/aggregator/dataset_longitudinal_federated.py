from typing import List

from sail_safe_functions.aggregator.data_model.data_model_longitudinal import DataModelLongitudinal
from sail_safe_functions.aggregator.reference_dataset_longitudinal import ReferenceDatasetLongitudinal


class DatasetLongitudinalFederated:
    def __init__(
        self,
        list_reference: List[ReferenceDatasetLongitudinal],
        data_model_longitudinal: DataModelLongitudinal,
    ) -> None:
        self.data_model_longitudinal = data_model_longitudinal
        self.dict_reference_dataset_longitudinal = {}
        for reference in list_reference:
            self._add_reference_dataset_longitudinal(reference)

    def _add_reference_dataset_longitudinal(self, data_frame_longitudinal: ReferenceDatasetLongitudinal):
        self.dict_reference_dataset_longitudinal[data_frame_longitudinal.dataset_id] = data_frame_longitudinal
