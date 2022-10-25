import uuid

from sail_safe_functions_orchestrator.data_frame import DataFrame
from sail_safe_functions_orchestrator.dataset_longitudinal import DatasetLongitudinal
from sail_safe_functions_orchestrator.dataset_tabular import DatasetTabular
from sail_safe_functions_orchestrator.reference_data_frame import ReferenceDataFrame
from sail_safe_functions_orchestrator.reference_dataset_longitudinal import ReferenceDatasetLongitudinal
from sail_safe_functions_orchestrator.reference_dataset_tabular import ReferenceDatasetTabular


class ServiceReference:
    def __init__(self) -> None:
        self.dict_reference = {}

        # TODO split the referencer into different types to enable series and dataframes and use random guids
        # (or allow set guids fro the computgrah)

    def __call__(self):
        raise TypeError("Singletons must be accessed through `get_instance()`.")

    def get_instance() -> "ServiceReference":
        try:
            print("get!!!")
            return ServiceReference._instance

        except AttributeError:
            print("Create!!!")
            ServiceReference._instance = ServiceReference()
            return ServiceReference._instance

    def reference_to_dataset_longitudinal(
        self,
        reference: ReferenceDatasetLongitudinal,
    ) -> DatasetLongitudinal:
        if not reference.dataset_id in self.dict_reference:
            raise ValueError(f"Dataset not loaded: {reference.dataset_id}")
        return self.dict_reference[reference.dataset_id]

    def dataset_longitudinal_to_reference(
        self, dataset_longitudinal: DatasetLongitudinal
    ) -> ReferenceDatasetLongitudinal:
        self.dict_reference[dataset_longitudinal.dataset_id] = dataset_longitudinal
        return ReferenceDatasetTabular(dataset_longitudinal.dataset_id, dataset_longitudinal.data_model)

    ###
    def dataset_tabular_to_reference(self, dataset_tabular: DatasetTabular) -> ReferenceDatasetTabular:
        self.dict_reference[dataset_tabular.dataset_id] = dataset_tabular
        return ReferenceDatasetTabular(dataset_tabular.dataset_id, dataset_tabular.data_model)

    def reference_to_dataset_tabular(
        self,
        reference: ReferenceDatasetLongitudinal,
    ) -> DatasetTabular:
        if not reference.dataset_id in self.dict_reference:
            raise ValueError(f"Dataset not loaded: {reference.dataset_id}")
        return self.dict_reference[reference.dataset_id]

    ###
    def generate_reference_id(self):
        return uuid.uuid4()

    def data_frame_to_reference(self, data_frame: DataFrame) -> ReferenceDatasetTabular:
        reference_id = self.generate_reference_id()
        self.dict_reference[reference_id] = data_frame
        return ReferenceDataFrame(reference_id, data_frame.data_model_data_frame)

    def reference_to_data_frame(
        self,
        reference: ReferenceDataFrame,
    ) -> DatasetTabular:
        if not reference.reference_id in self.dict_reference:
            raise ValueError(f"DataFrame not loaded: {reference.reference_id}")
        return self.dict_reference[reference.reference_id]
