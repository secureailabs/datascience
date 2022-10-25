from abc import ABC
from typing import List

from sail_safe_functions_orchestrator.data_model.data_model_series import DataModelSeries
from sail_safe_functions_orchestrator.reference_series import ReferenceSeries


class SeriesFederated(ABC):
    def __init__(self, list_reference: List[ReferenceSeries], data_model_series: DataModelSeries) -> None:
        self.data_model_series = data_model_series
        self.dict_reference_series = {}
        for reference in list_reference:
            self._add_reference_series(reference)

    def _add_reference_series(self, reference: ReferenceSeries):
        self.dict_reference_series[reference.reference_id] = reference

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
