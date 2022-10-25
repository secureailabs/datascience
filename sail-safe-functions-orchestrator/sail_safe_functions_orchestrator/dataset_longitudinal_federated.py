from re import S
from typing import List

from sail_safe_functions_test.helper_sail_safe_functions.service_client_local import ServiceClientLocal

from sail_safe_functions_orchestrator.data_model.data_model_longitudinal import DataModelLongitudinal
from sail_safe_functions_orchestrator.packager_dataset.packager_data_federation import PackagerDataFederation
from sail_safe_functions_orchestrator.packager_dataset.serializer_dataset_fhirv1 import SerializerDatasetFhirv1
from sail_safe_functions_orchestrator.reference_dataset_longitudinal import ReferenceDatasetLongitudinal
from sail_safe_functions_orchestrator.service_client import ServiceClient
from sail_safe_functions_orchestrator.service_reference import ServiceReference


class DatasetLongitudinalFederated:
    def __init__(
        self,
        service_client: ServiceClient,
        list_reference: List[ReferenceDatasetLongitudinal],
        data_model_longitudinal: DataModelLongitudinal,
    ) -> None:
        self.service_client = service_client
        self.data_model_longitudinal = data_model_longitudinal
        self.dict_reference_dataset_longitudinal = {}
        for reference in list_reference:
            self._add_reference_dataset_longitudinal(reference)

    def _add_reference_dataset_longitudinal(self, data_frame_longitudinal: ReferenceDatasetLongitudinal):
        self.dict_reference_dataset_longitudinal[data_frame_longitudinal.dataset_id] = data_frame_longitudinal

    # TODO move this to testing library
    @staticmethod
    def read_for_path_file(path_file_data_federation: str):
        # TODO call safe function via RPC ReadDatasetFhirv1Precompute
        packager = PackagerDataFederation()
        packager.prepare_data_federation(path_file_data_federation)
        dict_dataset_name_to_dataset_id = packager.get_dict_dataset_name_to_dataset_id(path_file_data_federation)
        data_model_longitudinal = {}
        serializer = SerializerDatasetFhirv1()
        list_reference = []
        for dataset_id in dict_dataset_name_to_dataset_id.values():
            dataset_longitudinal = serializer.read_dataset(dataset_id)
            list_reference.append(
                ServiceReference.get_instance().dataset_longitudinal_to_reference(dataset_longitudinal)
            )

        service_client_local = ServiceClientLocal()
        return DatasetLongitudinalFederated(service_client_local, list_reference, data_model_longitudinal)
