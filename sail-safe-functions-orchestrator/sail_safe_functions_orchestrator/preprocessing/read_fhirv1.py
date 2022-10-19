import json
import os
from typing import List

from sail_safe_functions.preprocessing.read_dataset_fhirv1 import ReadZipJsonFhirPrecompute
from sail_safe_functions_orchestrator.data_model_longitudinal import DataModelLongitudinal
from sail_safe_functions_orchestrator.dataset_longitudinal_federated import DataFrameLongitudinalFederated
from sail_safe_functions_orchestrator.dataset_longitudinal_federated_local import DataFrameLongitudinalFederatedLocal


def read_fhirv1(path_dir_data_federation: str) -> DataFrameLongitudinalFederated:
    return ReadFhirv1.run(path_dir_data_federation)


class ReadFhirv1:
    @staticmethod
    def run(path_dir_data_federation: str) -> DataFrameLongitudinalFederated:
        path_file_data_model = os.path.join(path_dir_data_federation, "data_model_longitudinal.json")
        list_path_file_zip_json_fhir = []
        for name_file in os.listdir(path_dir_data_federation):
            if name_file.endswith(".zip"):
                path_file = os.path.join(path_dir_data_federation, name_file)
                dataset_id = name_file.split(".")[0]
                list_path_file_zip_json_fhir.append((dataset_id, path_file))

        with open(path_file_data_model, "r") as file:
            data_model = DataModelLongitudinal.from_json(json.load(file))

        data_frame_longitudinal_federated = DataFrameLongitudinalFederatedLocal(data_model)
        for dataset_id, path_file_dataset in list_path_file_zip_json_fhir:
            data_frame_longitudinal_federated.add_data_frame_longitudinal(
                dataset_id, ReadFhirv1Precompute.run(path_file_dataset)
            )
        return data_frame_longitudinal_federated
