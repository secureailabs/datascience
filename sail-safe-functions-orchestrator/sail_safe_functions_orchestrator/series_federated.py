from abc import ABC
from typing import List

import numpy

from sail_safe_functions_orchestrator.data_model.data_model_series import DataModelSeries
from sail_safe_functions_orchestrator.reference_series import ReferenceSeries
from sail_safe_functions_orchestrator.service_client import ServiceClient
from sail_safe_functions_orchestrator.service_reference import ServiceReference


class SeriesFederated(ABC):
    def __init__(
        self, service_client: ServiceClient, list_reference: List[ReferenceSeries], data_model_series: DataModelSeries
    ) -> None:
        self.service_client = service_client
        self.data_model_series = data_model_series
        self.dict_reference_series = {}
        for reference in list_reference:
            self._add_reference_series(reference)

    def _add_reference_series(self, reference: ReferenceSeries):
        if reference.dataset_id in self.dict_reference_series:
            raise Exception(f"Duplicate Series for dataset_id: {reference.dataset_id}")
        self.dict_reference_series[reference.dataset_id] = reference

    @property
    def size(self):
        size = 0
        for series in self.dict_series.values():
            size += series.size
        return size

    def items(self):
        return self.dict_series.items()

    def create_new(self) -> "SeriesFederated":
        raise NotImplementedError()

    # TODO move to local client
    def to_numpy(self) -> numpy.ndarray:
        list_array_numpy = []
        for reference_series in self.dict_reference_series.values():
            series = ServiceReference.get_instance().reference_to_series(reference_series)
            list_array_numpy.append(series.to_numpy())
        return numpy.concatenate(list_array_numpy)
