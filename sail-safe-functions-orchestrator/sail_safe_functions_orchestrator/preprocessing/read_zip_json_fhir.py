import json
import os
from typing import List

from sail_safe_functions.preprocessing.read_zip_json_fhir_precompute import ReadZipJsonFhirPrecompute
from sail_safe_functions_orchestrator.data_frame_logitudinal_federated import DataFrameLogitudinalFederated
from sail_safe_functions_orchestrator.data_frame_logitudinal_federated_local import DataFrameLogitudinalFederatedLocal
from sail_safe_functions_orchestrator.data_model_logitudinal import DataModelLogitudinal


def read_zip_json_fhir(path_dir_data_federation: str) -> DataFrameLogitudinalFederated:
    return ReadZipJsonFhir.run(path_dir_data_federation)


class ReadZipJsonFhir:
    @staticmethod
    def run(path_dir_data_federation: str) -> DataFrameLogitudinalFederated:
        path_file_data_model = os.path.join(path_dir_data_federation, "data_model_logitudinal.json")
        list_path_file_zip_json_fhir = []
        for name_file in os.listdir(path_dir_data_federation):
            if name_file.endswith(".zip"):
                path_file = os.path.join(path_dir_data_federation, name_file)
                dataset_id = name_file.split(".")[0]
                list_path_file_zip_json_fhir.append((dataset_id, path_file))

        with open(path_file_data_model, "r") as file:
            data_model = DataModelLogitudinal.from_json(json.load(file))

        data_frame_logitudinal_federated = DataFrameLogitudinalFederatedLocal(data_model)
        for dataset_id, path_file_dataset in list_path_file_zip_json_fhir:
            data_frame_logitudinal_federated.add_data_frame_logitudinal(
                dataset_id, ReadZipJsonFhirPrecompute.run(path_file_dataset)
            )
        return data_frame_logitudinal_federated
