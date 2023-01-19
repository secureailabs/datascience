from typing import List

from sail_core.implementation_manager import ImplementationManager
from sail_safe_functions.aggregator.dataset_longitudinal_federated import DatasetLongitudinalFederated
from sail_safe_functions.participant.preprocessing.read_dataset_fhirv1_precompute import ReadDatasetFhirv1Precompute


def read_dataset_fhirv1(
    list_dataset_id: List[str],
) -> DatasetLongitudinalFederated:
    return ReadDatasetFhirv1.run(list_dataset_id)


class ReadDatasetFhirv1:
    """Federate wrapper safe function for the pandas concatenate"""

    @staticmethod
    def run(
        list_dataset_id: List[str],
    ) -> DatasetLongitudinalFederated:
        list_reference = []
        print(list_dataset_id)
        service_participant = ImplementationManager.get_instance().get_participant_service()
        for dataset_id in list_dataset_id:

            dataset_longitudinal_reference = service_participant.call(
                dataset_id, ReadDatasetFhirv1Precompute, dataset_id
            )

            list_reference.append(dataset_longitudinal_reference)
        data_model_longitudinal = list_reference[0].data_model_logitudinal  # TODO typo
        return DatasetLongitudinalFederated(list_reference, data_model_longitudinal)
