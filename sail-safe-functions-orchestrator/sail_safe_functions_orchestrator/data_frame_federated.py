from abc import ABC
from typing import List

from sail_safe_functions.preprocessing.select_data_frame_precompute import SelectDataFramePrecompute
from sail_safe_functions.preprocessing.select_series_precompute import SelectSeriesPrecompute

from sail_safe_functions_orchestrator.data_model.data_model_data_frame import DataModelDataFrame
from sail_safe_functions_orchestrator.reference_data_frame import ReferenceDataFrame
from sail_safe_functions_orchestrator.series_federated import SeriesFederated


class DataFrameFederated(ABC):
    def __init__(self, list_reference: List[ReferenceDataFrame], data_model_data_frame: DataModelDataFrame) -> None:
        self.data_model_data_frame = data_model_data_frame
        self.dict_reference_data_frame = {}
        for reference in list_reference:
            self._add_reference_data_frame(reference)

    def create_new(self) -> "DataFrameFederated":
        raise NotImplementedError()

    def _add_reference_data_frame(self, reference: ReferenceDataFrame):
        if reference.reference_id in self.dict_reference_data_frame:
            raise Exception(f"Duplicate data_frame such series: {reference.reference_id}")
        self.dict_reference_data_frame[reference.reference_id] = reference

    def get_series(self, series_name: str) -> SeriesFederated:
        if series_name not in self.data_model_data_frame.dict_data_model_series:
            raise Exception(f"No such series: {series_name}")
        list_reference = []
        for reference_data_frame in self.dict_reference_data_frame.values():
            list_reference.append(SelectSeriesPrecompute.run(reference_data_frame, series_name))
        return SeriesFederated(list_reference, self.data_model_data_frame[series_name])

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
        return self.data_model_data_frame.list_series_name

    # property section end
