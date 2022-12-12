from typing import List

from sail_safe_functions.preprocessing.read_dataset_csvv1_precompute import ReadDatasetCsvv1Precompute
from sail_safe_functions_orchestrator.dataset_tabular_federated import DatasetTabularFederated
from sail_safe_functions_orchestrator.service_client_base import ServiceClientBase


def read_dataset_csvv1(service_client: ServiceClientBase, list_dataset_id: List[str]) -> DatasetTabularFederated:
    return ReadDatasetCsvv1.run(service_client, list_dataset_id)


class ReadDatasetCsvv1:
    """Federate wrapper safe function for the pandas concatenate"""

    @staticmethod
    def run(service_client: ServiceClientBase, list_dataset_id: List[str]) -> DatasetTabularFederated:
        list_reference = []
        for dataset_id in list_dataset_id:
            client = service_client.get_client(dataset_id)
            dataset_longitudinal_reference = client.call(ReadDatasetCsvv1Precompute, dataset_id)
            list_reference.append(dataset_longitudinal_reference)
        data_model_tabular = list_reference[0].data_model_tabular
        return DatasetTabularFederated(service_client, list_reference, data_model_tabular)
