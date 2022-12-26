from abc import ABC
from typing import List

from sail_safe_functions.aggregator.data_model.data_model_data_frame import DataModelDataFrame
from sail_safe_functions.aggregator.reference_data_frame import ReferenceDataFrame
from sail_safe_functions.aggregator.series_federated import SeriesFederated
from sail_safe_functions.aggregator.service_client_base import ServiceClientBase
from sail_safe_functions.participant.preprocessing.select_series_precompute import SelectSeriesPrecompute


class DataFrameFederated:
    # TODO reverse data_model_data_frame and list reference
    def __init__(
        self,
        service_client: ServiceClientBase,
        list_reference: List[ReferenceDataFrame],
        data_model_data_frame: DataModelDataFrame,
    ) -> None:
        self._service_client = service_client
        self._data_model_data_frame = data_model_data_frame
        self._dict_reference_data_frame = {}
        for reference in list_reference:
            self._add_reference_data_frame(reference)

    def _add_reference_data_frame(self, reference: ReferenceDataFrame):
        if reference.dataset_id in self._dict_reference_data_frame:
            raise Exception(f"Duplicate data_frame for dataset_id: {reference.dataset_id}")
        self._dict_reference_data_frame[reference.dataset_id] = reference

    def get_series(self, series_name: str) -> SeriesFederated:
        if series_name not in self.data_model_data_frame.dict_data_model_series:
            raise Exception(f"No such series: {series_name}")
        list_reference = []
        for dataset_id, reference_data_frame in self._dict_reference_data_frame.items():
            client = self._service_client.get_client(dataset_id)
            reference_series = client.call(SelectSeriesPrecompute, reference_data_frame, series_name)
            list_reference.append(reference_series)
        return SeriesFederated(self.service_client, list_reference, self.data_model_data_frame[series_name])

    def get_reference_data_frame(self, dataset_id: str) -> ReferenceDataFrame:
        if dataset_id not in self._dict_reference_data_frame:
            raise Exception(f"No data_frame_reference for dataset_id: {dataset_id}")
        return self._dict_reference_data_frame[dataset_id]

    # index section start

    def __delitem__(self, key) -> None:
        raise NotImplementedError()

    def __getitem__(self, key) -> SeriesFederated:
        # TODO check key typing
        return self.get_series(key)

    def __setitem__(self, key, value):
        raise NotImplementedError()

    # index section end

    # property section start
    @property
    def list_series_name(self) -> List[str]:
        return self._data_model_data_frame.list_series_name

    @property
    def list_dataset_id(self):
        return list(self._dict_reference_data_frame.keys())

    @property
    def data_model_data_frame(self) -> DataModelDataFrame:
        return self._data_model_data_frame

    @property
    def service_client(self) -> ServiceClientBase:
        return self._service_client

    @property
    def dict_reference_data_frame(self):
        return self._dict_reference_data_frame.copy()  # TODO place holder, remove this in the next refactor

    # property section end
