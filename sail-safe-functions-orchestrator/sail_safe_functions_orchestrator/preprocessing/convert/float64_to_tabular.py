from sail_safe_functions.preprocessing.convert.float64_to_tabular_precompute import Float64ToTabularPrecompute
from sail_safe_functions_orchestrator.data_frame_federated import DataFrameFederated
from sail_safe_functions_orchestrator.data_model.data_model_data_frame import DataModelDataFrame
from sail_safe_functions_orchestrator.tools_common import check_instance


def float64_to_tabular(
    data_frame_source: DataFrameFederated, data_model_target: DataModelDataFrame
) -> DataFrameFederated:
    """
    The function convert the float64 value to tabular value

        :param data_frame_source: Federated Data frame
        :type data_frame_source: DataFrameFederated
        :param data_model_target: The targeted data model
        :type data_model_target: DataModelDataFrame
        :return: tabular data
        :rtype: DataFrameFederated
    """
    return Float64ToTabular.run(data_frame_source, data_model_target)


class Float64ToTabular:
    def run(data_frame_source: DataFrameFederated, data_model_target: DataModelDataFrame) -> DataFrameFederated:
        check_instance(data_frame_source, DataFrameFederated)
        check_instance(data_model_target, DataModelDataFrame)

        list_reference = []
        for dataset_id in data_frame_source.list_dataset_id:
            client = data_frame_source.service_client.get_client(dataset_id)
            reference_data_frame = data_frame_source.dict_reference_data_frame[dataset_id]
            list_reference.append(client.call(Float64ToTabularPrecompute, reference_data_frame, data_model_target))

        return DataFrameFederated(
            data_frame_source.service_client, list_reference, list_reference[0].data_model_data_frame
        )
