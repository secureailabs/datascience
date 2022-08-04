from sail_safe_functions_orchestrator import preprocessing
from sail_safe_functions_orchestrator.data_frame_federated import DataFrameFederated
from sail_safe_functions_orchestrator.data_frame_federated_source import DataFrameFederatedSource
from sail_safe_functions_test.helper_sail_safe_functions.data_frame_federated_local import DataFrameFederatedLocal


class DataFrameFederatedSourceJsonzipLocal(DataFrameFederatedSource):
    def __init__(self, list_path_file_jsonzip) -> None:
        self.list_path_file_jsonzip = list_path_file_jsonzip

    def create_data_frame(self, dict_feature_schema: dict) -> DataFrameFederated:
        data_frame_federated = preprocessing.read_jsonzip(
            DataFrameFederatedLocal(), self.list_path_file_jsonzip, dict_feature_schema
        )

        return data_frame_federated
