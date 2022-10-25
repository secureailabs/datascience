from typing import List

from sail_safe_functions_orchestrator.data_model.data_model_longitudinal import DataModelLongitudinal
from sail_safe_functions_orchestrator.dataset_longitudinal_federated import DatasetLongitudinalFederated
from sail_safe_functions_orchestrator.packager_dataset.packager_data_federation import PackagerDataFederation
from sail_safe_functions_orchestrator.packager_dataset.serializer_dataset_fhirv1 import SerializerDatasetFhirv1
from sail_safe_functions_orchestrator.reference_dataset_longitudinal import ReferenceDatasetLongitudinal
from sail_safe_functions_orchestrator.service_reference import ServiceReference


class DatasetLongitudinalFederatedLocal(DatasetLongitudinalFederated):
    def __init__(self, data_model_longitudinal: DataModelLongitudinal) -> None:
        super().__init__(data_model_longitudinal)
        self.dict_dataset_longitudinal = {}

    def add_data_frame_longitudinal(self, data_frame_longitudinal: ReferenceDatasetLongitudinal):
        self.dict_dataset_longitudinal[data_frame_longitudinal.dataset_id] = data_frame_longitudinal

    # TODO move this to testing library
    @staticmethod
    def read_for_path_file(path_file_data_federation: str):
        # TODO call safe function via RPC ReadDatasetFhirv1Precompute
        packager = PackagerDataFederation()
        packager.prepare_data_federation(path_file_data_federation)
        dict_dataset_name_to_dataset_id = packager.get_dict_dataset_name_to_dataset_id(path_file_data_federation)
        list_reference_dataset_longitudinal = []
        data_model_longitudinal = {}
        dataset_federated = DatasetLongitudinalFederatedLocal(data_model_longitudinal)
        for dataset_id in dict_dataset_name_to_dataset_id.values():
            serializer = SerializerDatasetFhirv1()
            dataset_longitudinal = serializer.read_dataset(dataset_id)
            reference = ServiceReference.get_instance().dataset_longitudinal_to_reference(dataset_longitudinal)
            dataset_federated.add_data_frame_longitudinal(reference)
        return dataset_federated
