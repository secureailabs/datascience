import uuid

from sail_safe_functions_orchestrator.data_frame_federated import DataFrameFederated
from sail_safe_functions_orchestrator.data_model.data_model_data_frame import (
    DataModelDataFrame,
)
from sail_safe_functions_orchestrator.data_model.data_model_tabular import (
    DataModelTabular,
)
from sail_safe_functions_orchestrator.dataset_tabular_federated import (
    DatasetTabularFederated,
)
from sail_safe_functions_orchestrator.series_federated import SeriesFederated
from sail_safe_functions_orchestrator.tools_common import check_instance


class TestServiceReference:
    __singleton_instance = None

    def __init__(self) -> None:
        self.dict_reference = {}

        # TODO split the referencer into different types?
        # (or allow set guids for the computgrah)

        # TODO all the references could be merged because we are not using the datamodel anyway

    def __call__(self):
        raise TypeError("Singletons must be accessed through `get_instance()`.")

    @classmethod
    def get_instance(service) -> "TestServiceReference":
        # check for the singleton instance
        if not service.__singleton_instance:
            if not service.__singleton_instance:
                service.__singleton_instance = service()

        # return the singleton instance
        return service.__singleton_instance

    def generate_reference_id(self) -> str:
        return str(uuid.uuid4())

    def federated_series_to_reference(self, federated_series: SeriesFederated) -> str:
        check_instance(federated_series, SeriesFederated)
        reference_id = self.generate_reference_id()
        self.dict_reference[reference_id] = federated_series
        return reference_id

    def reference_to_federated_series(self, reference: str) -> SeriesFederated:
        check_instance(reference, str)
        if reference not in self.dict_reference:
            raise ValueError(f"Federated Series not loaded: {reference.reference_id}")
        return self.dict_reference[reference]

    def federated_dataframe_to_reference(
        self, federated_series: DataFrameFederated
    ) -> str:
        check_instance(federated_series, DataFrameFederated)
        reference_id = self.generate_reference_id()
        self.dict_reference[reference_id] = federated_series
        return reference_id

    def reference_to_federated_dataframe(self, reference: str) -> DataFrameFederated:
        check_instance(reference, str)
        if reference not in self.dict_reference:
            raise ValueError(f"Federated Series not loaded: {reference}")
        return self.dict_reference[reference]

    def data_model_data_frame_to_reference(
        self, data_model_data_frame: DataModelDataFrame
    ) -> str:
        check_instance(data_model_data_frame, DataModelDataFrame)
        reference_id = self.generate_reference_id()
        self.dict_reference[reference_id] = data_model_data_frame
        return reference_id

    def reference_to_data_model_data_frame(self, reference: str) -> DataModelDataFrame:
        check_instance(reference, str)
        if reference not in self.dict_reference:
            raise ValueError(f"Data model data frame not loaded: {reference}")
        return self.dict_reference[reference]

    def data_model_tabular_to_reference(
        self, data_model_data_frame: DataModelTabular
    ) -> str:
        check_instance(data_model_data_frame, DataModelTabular)
        reference_id = self.generate_reference_id()
        self.dict_reference[reference_id] = data_model_data_frame
        return reference_id

    def reference_to_data_model_tabular(self, reference: str) -> DataModelTabular:
        check_instance(reference, str)
        if reference not in self.dict_reference:
            raise ValueError(f"Data model tabular not loaded: {reference}")
        return self.dict_reference[reference]

    def data_set_tabular_to_reference(
        self, data_model_data_frame: DatasetTabularFederated
    ) -> str:
        check_instance(data_model_data_frame, DatasetTabularFederated)
        reference_id = self.generate_reference_id()
        self.dict_reference[reference_id] = data_model_data_frame
        return reference_id

    def reference_to_data_set_tabular(self, reference: str) -> DatasetTabularFederated:
        check_instance(reference, str)
        if reference not in self.dict_reference:
            raise ValueError(f"Data model tabular not loaded: {reference}")
        return self.dict_reference[reference]
