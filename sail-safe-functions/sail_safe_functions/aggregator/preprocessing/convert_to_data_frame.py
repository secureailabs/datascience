from sail_core.implementation_manager import ImplementationManager
from sail_core.tools_common import check_instance
from sail_safe_functions.aggregator.data_frame_federated import DataFrameFederated
from sail_safe_functions.aggregator.data_model.data_model_data_frame import DataModelDataFrame
from sail_safe_functions.aggregator.dataset_longitudinal_federated import DatasetLongitudinalFederated
from sail_safe_functions.participant.preprocessing.convert_to_data_frame_precompute import ConvertToDataFramePrecompute
from sail_safe_functions.safe_function_base import SafeFunctionBase


def convert_to_data_frame(
    dataset_source: DatasetLongitudinalFederated,
    data_model_data_frame: DataModelDataFrame,
) -> DataFrameFederated:
    return ConvertToDataFrame.run(dataset_source, data_model_data_frame)


class ConvertToDataFrame(SafeFunctionBase):
    @staticmethod
    def run(
        dataset_source: DatasetLongitudinalFederated,
        data_model_data_frame: DataModelDataFrame,
    ) -> DataFrameFederated:
        check_instance(dataset_source, DatasetLongitudinalFederated)
        check_instance(data_model_data_frame, DataModelDataFrame)

        list_reference = []
        participant_service = ImplementationManager.get_instance().get_participant_service()
        for dataset_id, dataset_refrence in dataset_source.dict_reference_dataset_longitudinal.items():
            dataset_tabular_reference = participant_service.call(
                dataset_id,
                ConvertToDataFramePrecompute,
                dataset_refrence,
                data_model_data_frame,
            )
            list_reference.append(dataset_tabular_reference)
        return DataFrameFederated(list_reference, data_model_data_frame)
