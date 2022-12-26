from typing import List

from sail_safe_functions.aggregator.dataset_longitudinal_federated import DatasetLongitudinalFederated
from sail_safe_functions.aggregator.service_client_base import ServiceClientBase
from sail_safe_functions.participant.preprocessing.read_dataset_fhirv1_precompute import ReadDatasetFhirv1Precompute


def read_dataset_fhirv1(service_client: ServiceClientBase, list_dataset_id: List[str]) -> DatasetLongitudinalFederated:
    return ReadDatasetFhirv1.run(service_client, list_dataset_id)


class ReadDatasetFhirv1:
    """Federate wrapper safe function for the pandas concatenate"""

    @staticmethod
    def run(service_client: ServiceClientBase, list_dataset_id: List[str]) -> DatasetLongitudinalFederated:
        list_reference = []
        for dataset_id in list_dataset_id:
            client = service_client.get_client(dataset_id)
            dataset_longitudinal_reference = client.call(ReadDatasetFhirv1Precompute, dataset_id)
            list_reference.append(dataset_longitudinal_reference)
        data_model_longitudinal = list_reference[0].data_model_logitudinal  # TODO typo
        return DatasetLongitudinalFederated(service_client, list_reference, data_model_longitudinal)
