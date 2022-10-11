from sail_safe_functions.preprocessing.convert_to_dataset_tabular_precompute import ConvertToDatasetTabularPrecompute
from sail_safe_functions_orchestrator.data_frame_federated import DataFrameFederated
from sail_safe_functions_orchestrator.data_model.data_model_tabular import DataModelTabular
from sail_safe_functions_orchestrator.dataset_longitudinal_federated import DatasetLongitudinalFederated
from sail_safe_functions_orchestrator.dataset_tabular_federated import DatasetTabularFederated
from sail_safe_functions_orchestrator.tools_common import check_instance


def convert_to_dataset_tabular(
    dataset_source: DatasetLongitudinalFederated,
    dataset_federation_id: str,
    dataset_federation_name: str,
    data_model_tabular: DataModelTabular,
) -> DatasetTabularFederated:
    return ConvertToDatasetTabular.run(
        dataset_source, dataset_federation_id, dataset_federation_name, data_model_tabular
    )


class ConvertToDatasetTabular:
    def run(
        dataset_source: DatasetLongitudinalFederated,
        dataset_federation_id: str,
        dataset_federation_name: str,
        data_model_tabular: DataModelTabular,
    ) -> DataFrameFederated:
        check_instance(dataset_source, DatasetLongitudinalFederated)
        check_instance(dataset_federation_id, str)
        check_instance(dataset_federation_name, str)
        check_instance(data_model_tabular, DataModelTabular)

        list_reference = []
        for dataset_id, dataset_refrence in dataset_source.dict_reference_dataset_longitudinal.items():
            dataset_name = dataset_id  # TODO fix this
            client = dataset_source.service_client.get_client(dataset_id)
            dataset_tabular_reference = client.call(ConvertToDatasetTabularPrecompute,
                    dataset_refrence,
                    dataset_federation_id,
                    dataset_federation_name,
                    dataset_id,
                    dataset_name,
                    data_model_tabular)
            list_reference.append(dataset_tabular_reference)
        return DatasetTabularFederated(dataset_source.service_client, list_reference, data_model_tabular)
