from abc import ABC
from typing import Any, Dict, List, Type

import numpy
from sail_core.implementation_manager import ImplementationManager
from sail_safe_functions.aggregator.data_model.data_model_series import DataModelSeries
from sail_safe_functions.aggregator.reference_series import ReferenceSeries
from sail_safe_functions.aggregator.service_reference import ServiceReference


class SeriesFederated:
    def __init__(
        self,
        list_reference: List[ReferenceSeries],
        data_model_series: DataModelSeries,
    ) -> None:
        self.__data_model_series: DataModelSeries = data_model_series
        self.__dict_reference_series: Dict[str, ReferenceSeries] = {}
        for reference in list_reference:
            self._add_reference_series(reference)

    def _add_reference_series(self, reference: ReferenceSeries):
        if reference.dataset_id in self.__dict_reference_series:
            raise Exception(f"Duplicate Series for dataset_id: {reference.dataset_id}")
        self.__dict_reference_series[reference.dataset_id] = reference

    def get_reference_series(self, dataset_id: str) -> ReferenceSeries:
        if dataset_id not in self.__dict_reference_series:
            raise Exception(f"No series_reference for dataset_id: {dataset_id}")
        return self.__dict_reference_series[dataset_id]

    def map_function(self, function: Type, *argument_list, **argument_dict) -> List[Any]:
        participant_service = ImplementationManager.get_instance().get_participant_service()
        list_result = []
        for dataset_id, reference_series in self.__dict_reference_series.items():
            list_result.append(
                participant_service.call(dataset_id, function, reference_series, *argument_list, **argument_dict)
            )
        return list_result

    # property section start
    @property
    def list_dataset_id(self):
        return list(self.__dict_reference_series.keys())

    @property
    def series_name(self):
        return self.data_model_series.series_name

    @property
    def data_model_series(self) -> DataModelSeries:
        return self.__data_model_series

    @property
    def dict_reference_series(self):
        return self.__dict_reference_series.copy()  # TODO place holder remove this in the next refactor

    # property section end

    # TODO move to local client
    def to_numpy(self) -> numpy.ndarray:
        list_array_numpy = []
        for reference_series in self.dict_reference_series.values():
            series = ServiceReference.get_instance().reference_to_series(reference_series)
            list_array_numpy.append(series.to_numpy())
        return numpy.concatenate(list_array_numpy)
