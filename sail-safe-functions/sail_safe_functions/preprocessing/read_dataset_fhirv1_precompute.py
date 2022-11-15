from sail_safe_functions_orchestrator.packager_dataset.serializer_dataset_fhirv1 import SerializerDatasetFhirv1
from sail_safe_functions_orchestrator.reference_dataset_longitudinal import ReferenceDatasetLongitudinal
from sail_safe_functions_orchestrator.service_reference import ServiceReference


class ReadDatasetFhirv1Precompute:
    def run(dataset_id: str) -> ReferenceDatasetLongitudinal:
        serializer = SerializerDatasetFhirv1()
        dataset_longitudinal = serializer.read_dataset(dataset_id)
        ServiceReference.get_instance().dataset_longitudinal_to_reference(dataset_longitudinal)
        return ReferenceDatasetLongitudinal(dataset_id)
