import json

from sail_safe_functions_orchestrator.dataset_longitudinal import DataFrameLongitudinal
from sail_safe_functions_orchestrator.packager_dataset.serializer_dataset_fhirv1 import SerializerDatasetFhirv1


class ReadDatasetFhirv1Precompute:
    def run(path_file_jsonzip_source: str) -> DataFrameLongitudinal:
        packager = SerializerDatasetFhirv1()
        return packager.read_dataset_longitudinal(path_file_jsonzip_source)
