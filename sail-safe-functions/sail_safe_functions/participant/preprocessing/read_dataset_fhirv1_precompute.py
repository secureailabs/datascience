from sail_safe_functions.aggregator.packager_dataset.serializer_dataset_fhirv1 import SerializerDatasetFhirv1
from sail_safe_functions.aggregator.reference_dataset_longitudinal import ReferenceDatasetLongitudinal
from sail_safe_functions.aggregator.service_reference import ServiceReference
from sail_safe_functions.safe_function_base import SafeFunctionBase


class ReadDatasetFhirv1Precompute(SafeFunctionBase):
    def run(dataset_id: str) -> ReferenceDatasetLongitudinal:
        serializer = SerializerDatasetFhirv1()
        dataset_longitudinal = serializer.read_dataset(dataset_id)
        return ServiceReference.get_instance().dataset_longitudinal_to_reference(dataset_longitudinal)
