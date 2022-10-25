from typing import List

from sail_safe_functions.preprocessing.select_data_frame_precompute import SelectDataFramePrecompute

from sail_safe_functions_orchestrator.data_frame_federated import DataFrameFederated
from sail_safe_functions_orchestrator.data_model.data_model_tabular import DataModelTabular
from sail_safe_functions_orchestrator.reference_dataset_tabular import ReferenceDatasetTabular


class DatasetTabularFederated:
    def __init__(self, list_reference: List[ReferenceDatasetTabular], data_model_tabular: DataModelTabular) -> None:
        self.data_model_tabular = data_model_tabular
        self.dict_reference_dataset_tabular = {}
        for reference in list_reference:
            self._add_reference_dataset_tabular(reference)

    def _add_reference_dataset_tabular(self, reference: ReferenceDatasetTabular):
        self.dict_reference_dataset_tabular[reference.dataset_id] = reference

    def get_data_frame(self, data_frame_name: str) -> DataFrameFederated:
        if data_frame_name not in self.data_model_tabular.dict_data_model_data_frame:
            raise Exception(f"No such data_frame: {data_frame_name}")
        list_reference = []
        for reference_dataset_tabular in self.dict_reference_dataset_tabular.values():
            list_reference.append(SelectDataFramePrecompute.run(reference_dataset_tabular, data_frame_name))
        return DataFrameFederated(list_reference, self.data_model_tabular[data_frame_name])

    # index section start

    def __delitem__(self, key) -> None:
        raise NotImplementedError()

    def __getitem__(self, key) -> DataFrameFederated:
        # TODO check key typing
        return self.get_data_frame(key)

    def __setitem__(self, key, value):
        raise NotImplementedError()

    # index section end

    # property section start
    @property
    def list_data_frame_name(self) -> List[str]:
        return self.data_model_tabular.list_data_frame_name

    # property section end
