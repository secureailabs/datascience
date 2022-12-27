from typing import Any, List, Type

from sail_core.implementation_manager import ImplementationManager
from sail_safe_functions.aggregator.data_frame_federated import DataFrameFederated
from sail_safe_functions.aggregator.data_model.data_model_tabular import DataModelTabular
from sail_safe_functions.aggregator.reference_dataset_tabular import ReferenceDatasetTabular
from sail_safe_functions.participant.preprocessing.select_data_frame_precompute import SelectDataFramePrecompute


class DatasetTabularFederated:
    def __init__(
        self,
        list_reference: List[ReferenceDatasetTabular],
        data_model_tabular: DataModelTabular,
    ) -> None:
        self.__data_model_tabular = data_model_tabular
        self.__dict_reference_dataset_tabular = {}
        for reference in list_reference:
            self._add_reference_dataset_tabular(reference)

    def _add_reference_dataset_tabular(self, reference: ReferenceDatasetTabular):
        self.__dict_reference_dataset_tabular[reference.dataset_id] = reference

    def map_function(self, function: Type, *argument_list, **argument_dict) -> List[Any]:
        participant_service = ImplementationManager.get_instance().get_participant_service()
        list_result = []
        for dataset_id, reference_data_frame in self.__dict_reference_dataset_tabular.items():
            list_result.append(
                participant_service.call(dataset_id, function, reference_data_frame, argument_list, argument_dict)
            )
        return list_result

    def get_data_frame(self, data_frame_name: str) -> DataFrameFederated:
        if data_frame_name not in self.data_model_tabular.dict_data_model_data_frame:
            raise Exception(f"No such data_frame: {data_frame_name}")
        list_reference = self.map_function(SelectDataFramePrecompute, data_frame_name)

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

    @property
    def data_model_tabular(self) -> DataModelTabular:
        return self.__data_model_tabular

    # property section end
