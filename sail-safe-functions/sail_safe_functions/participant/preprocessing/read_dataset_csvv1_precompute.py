from sail_safe_functions.aggregator.packager_dataset.serializer_dataset_csvv1 import SerializerDatasetCsvv1
from sail_safe_functions.aggregator.reference_dataset_tabular import ReferenceDatasetTabular
from sail_safe_functions.aggregator.service_reference import ServiceReference
from sail_safe_functions.safe_function_base import SafeFunctionBase


class ReadDatasetCsvv1Precompute(SafeFunctionBase):
    @staticmethod
    def run(dataset_id: str) -> ReferenceDatasetTabular:
        serializer = SerializerDatasetCsvv1()
        dataset_tabular = serializer.read_dataset(dataset_id)
        return ServiceReference.get_instance().dataset_tabular_to_reference(dataset_tabular)
