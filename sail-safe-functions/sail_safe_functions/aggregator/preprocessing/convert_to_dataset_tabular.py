from sail_safe_functions.aggregator.data_model.data_model_tabular import DataModelTabular
from sail_safe_functions.aggregator.dataset_longitudinal_federated import DatasetLongitudinalFederated
from sail_safe_functions.aggregator.dataset_tabular_federated import DatasetTabularFederated
from sail_safe_functions.aggregator.tools_common import check_instance
from sail_safe_functions.participant.preprocessing.convert_to_dataset_tabular_precompute import (
    ConvertToDatasetTabularPrecompute,
)
from sail_safe_functions.safe_function_base import SafeFunctionBase


def convert_to_dataset_tabular(
    dataset_source: DatasetLongitudinalFederated,
    dataset_federation_id: str,
    dataset_federation_name: str,
    data_model_tabular: DataModelTabular,
) -> DatasetTabularFederated:
    return ConvertToDatasetTabular.run(
        dataset_source, dataset_federation_id, dataset_federation_name, data_model_tabular
    )


class ConvertToDatasetTabular(SafeFunctionBase):
    @staticmethod
    def run(
        dataset_source: DatasetLongitudinalFederated,
        dataset_federation_id: str,
        dataset_federation_name: str,
        data_model_tabular: DataModelTabular,
    ) -> DatasetTabularFederated:
        check_instance(dataset_source, DatasetLongitudinalFederated)
        check_instance(dataset_federation_id, str)
        check_instance(dataset_federation_name, str)
        check_instance(data_model_tabular, DataModelTabular)

        list_reference = []
        for dataset_id, dataset_refrence in dataset_source.dict_reference_dataset_longitudinal.items():
            dataset_name = dataset_id  # TODO fix this
            client = dataset_source.service_client.get_client(dataset_id)
            dataset_tabular_reference = client.call(
                ConvertToDatasetTabularPrecompute,
                dataset_refrence,
                dataset_federation_id,
                dataset_federation_name,
                dataset_id,
                dataset_name,
                data_model_tabular,
            )
            list_reference.append(dataset_tabular_reference)
        return DatasetTabularFederated(dataset_source.service_client, list_reference, data_model_tabular)
