import uuid

from sail_core.tools_common import check_instance
from sail_safe_functions.aggregator.data_frame_federated import DataFrameFederated
from sail_safe_functions.aggregator.data_model.data_model_data_frame import DataModelDataFrame
from sail_safe_functions.aggregator.data_model.data_model_series import DataModelSeries
from sail_safe_functions.aggregator.data_model.data_model_tabular import DataModelTabular
from sail_safe_functions.aggregator.dataset_longitudinal_federated import DatasetLongitudinalFederated
from sail_safe_functions.aggregator.dataset_tabular_federated import DatasetTabularFederated
from sail_safe_functions.aggregator.series_federated import SeriesFederated


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

    def federated_longitudinal_data_to_reference(self, federated_longitudinal: DatasetLongitudinalFederated) -> str:
        check_instance(federated_longitudinal, DatasetLongitudinalFederated)
        reference_id = self.generate_reference_id()
        self.dict_reference[reference_id] = federated_longitudinal
        return reference_id

    def reference_to_federated_longitudinal_data(self, reference: str) -> DatasetLongitudinalFederated:
        check_instance(reference, str)
        if reference not in self.dict_reference:
            raise ValueError(f"Federated Longitudinal Data not loaded: {reference}")
        return self.dict_reference[reference]

    def data_model_series_to_reference(self, series_model: DataModelSeries) -> str:
        check_instance(series_model, DataModelSeries)
        reference_id = self.generate_reference_id()
        self.dict_reference[reference_id] = series_model
        return reference_id

    def reference_to_data_model_series(self, reference: str) -> str:
        check_instance(reference, str)
        if reference not in self.dict_reference:
            raise ValueError(f"Series Model not loaded: {reference}")
        return self.dict_reference[reference]

    def federated_series_to_reference(self, federated_series: SeriesFederated) -> str:
        check_instance(federated_series, SeriesFederated)
        reference_id = self.generate_reference_id()
        self.dict_reference[reference_id] = federated_series
        return reference_id

    def reference_to_federated_series(self, reference: str) -> SeriesFederated:
        check_instance(reference, str)
        if reference not in self.dict_reference:
            raise ValueError(f"Federated Series not loaded: {reference}")
        return self.dict_reference[reference]

    def federated_dataframe_to_reference(self, federated_series: DataFrameFederated) -> str:
        check_instance(federated_series, DataFrameFederated)
        reference_id = self.generate_reference_id()
        self.dict_reference[reference_id] = federated_series
        return reference_id

    def reference_to_federated_dataframe(self, reference: str) -> DataFrameFederated:
        check_instance(reference, str)
        if reference not in self.dict_reference:
            raise ValueError(f"Federated Series not loaded: {reference}")
        return self.dict_reference[reference]

    def data_model_data_frame_to_reference(self, data_model_data_frame: DataModelDataFrame) -> str:
        check_instance(data_model_data_frame, DataModelDataFrame)
        reference_id = self.generate_reference_id()
        self.dict_reference[reference_id] = data_model_data_frame
        return reference_id

    def reference_to_data_model_data_frame(self, reference: str) -> DataModelDataFrame:
        check_instance(reference, str)
        if reference not in self.dict_reference:
            raise ValueError(f"Data model data frame not loaded: {reference}")
        return self.dict_reference[reference]

    def data_model_tabular_to_reference(self, data_model_data_frame: DataModelTabular) -> str:
        check_instance(data_model_data_frame, DataModelTabular)
        reference_id = self.generate_reference_id()
        self.dict_reference[reference_id] = data_model_data_frame
        return reference_id

    def reference_to_data_model_tabular(self, reference: str) -> DataModelTabular:
        check_instance(reference, str)
        if reference not in self.dict_reference:
            raise ValueError(f"Data model tabular not loaded: {reference}")
        return self.dict_reference[reference]

    def data_set_tabular_to_reference(self, data_model_data_frame: DatasetTabularFederated) -> str:
        check_instance(data_model_data_frame, DatasetTabularFederated)
        reference_id = self.generate_reference_id()
        self.dict_reference[reference_id] = data_model_data_frame
        return reference_id

    def reference_to_data_set_tabular(self, reference: str) -> DatasetTabularFederated:
        check_instance(reference, str)
        if reference not in self.dict_reference:
            raise ValueError(f"Data model tabular not loaded: {reference}")
        return self.dict_reference[reference]
