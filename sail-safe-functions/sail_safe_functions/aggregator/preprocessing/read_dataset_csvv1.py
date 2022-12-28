from typing import List

from sail_core.implementation_manager import ImplementationManager
from sail_safe_functions.aggregator.dataset_tabular_federated import DatasetTabularFederated
from sail_safe_functions.participant.preprocessing.read_dataset_csvv1_precompute import ReadDatasetCsvv1Precompute


def read_dataset_csvv1(
    list_dataset_id: List[str],
) -> DatasetTabularFederated:
    return ReadDatasetCsvv1.run(list_dataset_id)


class ReadDatasetCsvv1:
    """Federate wrapper safe function for the pandas concatenate"""

    @staticmethod
    def run(
        list_dataset_id: List[str],
    ) -> DatasetTabularFederated:
        list_reference = []
        service_participant = ImplementationManager.get_instance().get_participant_service()
        for dataset_id in list_dataset_id:

            dataset_tabular_reference = service_participant.call(dataset_id, ReadDatasetCsvv1Precompute, dataset_id)
            list_reference.append(dataset_tabular_reference)
        data_model_tabular = list_reference[0].data_model_tabular
        return DatasetTabularFederated(list_reference, data_model_tabular)
