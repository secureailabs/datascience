from typing import List

from sail_safe_functions.preprocessing.select_data_frame_precompute import SelectDataFramePrecompute

from sail_safe_functions_orchestrator.data_frame_federated import DataFrameFederated
from sail_safe_functions_orchestrator.data_model.data_model_tabular import DataModelTabular
from sail_safe_functions_orchestrator.reference_dataset_tabular import ReferenceDatasetTabular
from sail_safe_functions_orchestrator.service_client_base import ServiceClientBase


class DatasetTabularFederated:
    def __init__(
        self,
        service_client: ServiceClientBase,
        list_reference: List[ReferenceDatasetTabular],
        data_model_tabular: DataModelTabular,
    ) -> None:
        self._service_client = service_client
        self._data_model_tabular = data_model_tabular
        self._dict_reference_dataset_tabular = {}
        for reference in list_reference:
            self._add_reference_dataset_tabular(reference)

    def _add_reference_dataset_tabular(self, reference: ReferenceDatasetTabular):
        self._dict_reference_dataset_tabular[reference.dataset_id] = reference

    def get_data_frame(self, data_frame_name: str) -> DataFrameFederated:
        if data_frame_name not in self.data_model_tabular.dict_data_model_data_frame:
            raise Exception(f"No such data_frame: {data_frame_name}")
        list_reference = []
        for dataset_id, reference_dataset_tabular in self._dict_reference_dataset_tabular.items():
            client = self.service_client.get_client(dataset_id)
            reference_data_frame = client.call(SelectDataFramePrecompute, reference_dataset_tabular, data_frame_name)
            list_reference.append(reference_data_frame)
        return DataFrameFederated(self.service_client, list_reference, self.data_model_tabular[data_frame_name])

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

    @property
    def data_model_tabular(self) -> DataModelTabular:
        return self._data_model_tabular

        
    @property
    def service_client(self) -> ServiceClientBase:
        return self._service_client
    # property section end
