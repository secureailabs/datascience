from abc import ABC
from typing import List

import numpy
from sail_safe_functions_orchestrator.data_model.data_model_series import DataModelSeries
from sail_safe_functions_orchestrator.reference_series import ReferenceSeries
from sail_safe_functions_orchestrator.service_client_base import ServiceClientBase
from sail_safe_functions_orchestrator.service_reference import ServiceReference


class SeriesFederated:
    def __init__(
        self,
        service_client: ServiceClientBase,
        list_reference: List[ReferenceSeries],
        data_model_series: DataModelSeries,
    ) -> None:
        self._service_client = service_client
        self._data_model_series = data_model_series
        self._dict_reference_series = {}
        for reference in list_reference:
            self._add_reference_series(reference)

    def _add_reference_series(self, reference: ReferenceSeries):
        if reference.dataset_id in self._dict_reference_series:
            raise Exception(f"Duplicate Series for dataset_id: {reference.dataset_id}")
        self._dict_reference_series[reference.dataset_id] = reference

    def get_reference_series(self, dataset_id: str) -> ReferenceSeries:
        if dataset_id not in self._dict_reference_series:
            raise Exception(f"No series_reference for dataset_id: {dataset_id}")
        return self._dict_reference_series[dataset_id]

    # property section start
    @property
    def list_dataset_id(self):
        return list(self._dict_reference_series.keys())

    @property
    def series_name(self):
        return self.data_model_series.series_name

    @property
    def data_model_series(self) -> DataModelSeries:
        return self._data_model_series

    @property
    def service_client(self) -> ServiceClientBase:
        return self._service_client

    @property
    def dict_reference_series(self):
        return self._dict_reference_series.copy()  # TODO place holder remove this in the next refactor

    # property section end

    # TODO move to local client
    def to_numpy(self) -> numpy.ndarray:
        list_array_numpy = []
        for reference_series in self.dict_reference_series.values():
            series = ServiceReference.get_instance().reference_to_series(reference_series)
            list_array_numpy.append(series.to_numpy())
        return numpy.concatenate(list_array_numpy)
