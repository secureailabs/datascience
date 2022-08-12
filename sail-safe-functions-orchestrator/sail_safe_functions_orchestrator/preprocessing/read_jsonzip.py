from typing import List

from sail_safe_functions.preprocessing.read_jsonzip_precompute import ReadJsonzipPrecompute
from sail_safe_functions_orchestrator.data_frame_federated import DataFrameFederated
from sail_safe_functions_orchestrator.tools_common import check_instance


def read_jsonzip(
    data_frame_prototype: DataFrameFederated, list_path_file_jsonzip: List[str], dict_feature_schema: dict
) -> DataFrameFederated:
    return ReadJsonzip.run(data_frame_prototype, list_path_file_jsonzip, dict_feature_schema)


class ReadJsonzip:
    """
    Drop rows or columns with missing data
    """

    def run(
        data_frame_prototype: DataFrameFederated, list_path_file_jsonzip: List[str], dict_feature_schema: dict
    ) -> DataFrameFederated:

        check_instance(data_frame_prototype, DataFrameFederated)
        check_instance(list_path_file_jsonzip, list)
        check_instance(dict_feature_schema, dict)
        data_frame_federated = data_frame_prototype.create_new()
        for path_file_jsonzip in list_path_file_jsonzip:
            data_frame = ReadJsonzipPrecompute.run(path_file_jsonzip, dict_feature_schema)
            data_frame_federated.add_data_frame(path_file_jsonzip, data_frame)
        return data_frame_federated
