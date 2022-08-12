from typing import Any, List

from sail_safe_functions.preprocessing.query_precompute import QueryPrecompute
from sail_safe_functions.preprocessing.read_jsonzip_precompute import ReadJsonzipPrecompute
from sail_safe_functions_orchestrator.data_frame_federated import DataFrameFederated
from sail_safe_functions_orchestrator.tools_common import check_instance


def query(data_frame_source: DataFrameFederated, query_expresion: Any) -> DataFrameFederated:
    return Query.run(data_frame_source, query_expresion)


class Query:
    """
    Drop rows or columns with missing data
    """

    def run(data_frame_source: DataFrameFederated, query_expresion: Any) -> DataFrameFederated:

        check_instance(data_frame_source, DataFrameFederated)
        # check_instance(query_expresion, list) #TODO
        data_frame_target = data_frame_source.create_new()
        for dataset_id in data_frame_source.dict_dataframe:
            data_frame_target.dict_dataframe[dataset_id] = QueryPrecompute.run(
                data_frame_source.dict_dataframe[dataset_id], query_expresion
            )
        return data_frame_target
