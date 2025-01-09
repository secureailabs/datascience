from abc import ABC
from typing import Any, Dict, List, Type

from sail_core.implementation_manager import ImplementationManager
from sail_safe_functions.aggregator.data_model.data_model_data_frame import DataModelDataFrame
from sail_safe_functions.aggregator.reference_data_frame import ReferenceDataFrame
from sail_safe_functions.aggregator.series_federated import SeriesFederated
from sail_safe_functions.participant.preprocessing.select_series_precompute import SelectSeriesPrecompute


class DataFrameFederated:
    # TODO reverse data_model_data_frame and list reference
    def __init__(
        self,
        list_reference: List[ReferenceDataFrame],
        data_model_data_frame: DataModelDataFrame,
    ) -> None:
        self.__data_model_data_frame = data_model_data_frame
        self.__dict_reference_data_frame = {}
        for reference in list_reference:
            self._add_reference_data_frame(reference)

    def _add_reference_data_frame(self, reference: ReferenceDataFrame):
        if reference.dataset_id in self.__dict_reference_data_frame:
            raise Exception(f"Duplicate data_frame for dataset_id: {reference.dataset_id}")
        self.__dict_reference_data_frame[reference.dataset_id] = reference

    def map_function(self, function: Type, *argument_list, **argument_dict) -> List[Any]:
        participant_service = ImplementationManager.get_instance().get_participant_service()
        list_result = []
        for dataset_id, reference_data_frame in self.__dict_reference_data_frame.items():
            list_result.append(
                participant_service.call(dataset_id, function, reference_data_frame, *argument_list, **argument_dict)
            )
        return list_result

    def get_series(self, series_name: str) -> SeriesFederated:
        if series_name not in self.data_model_data_frame.dict_data_model_series:
            raise Exception(f"No such series: {series_name}")
        list_reference = self.map_function(SelectSeriesPrecompute, series_name)
        return SeriesFederated(list_reference, self.data_model_data_frame[series_name])

    def get_reference_data_frame(self, dataset_id: str) -> ReferenceDataFrame:
        if dataset_id not in self.__dict_reference_data_frame:
            raise Exception(f"No data_frame_reference for dataset_id: {dataset_id}")
        return self.__dict_reference_data_frame[dataset_id]

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
    def data_frame_name(self) -> str:
        return self.__data_model_data_frame.data_frame_name

    @property
    def list_series_name(self) -> List[str]:
        return self.__data_model_data_frame.list_series_name

    @property
    def list_dataset_id(self):
        return list(self.__dict_reference_data_frame.keys())

    @property
    def data_model_data_frame(self) -> DataModelDataFrame:
        return self.__data_model_data_frame

    @property
    def dict_reference_data_frame(self):
        return self.__dict_reference_data_frame.copy()  # TODO place holder, remove this in the next refactor

    # property section end
