from typing import Any, List

from sail_safe_functions.privacy_barrier.pragmatic_noise_precompute import PragmaticNoisePrecompute
from sail_safe_functions_orchestrator.data_frame_federated import DataFrameFederated
from sail_safe_functions_orchestrator.tools_common import check_instance


def pragmatic_noise(data_frame_source: DataFrameFederated, query_expresion: Any) -> DataFrameFederated:
    """
    > The function `pragmatic_noise` takes a `DataFrameFederated` and a query expression and returns a
    `DataFrameFederated`

    :param data_frame_source: DataFrameFederated
    :type data_frame_source: DataFrameFederated
    :param query_expresion: Any
    :type query_expresion: Any
    :return: A DataFrameFederated object
    """
    # A placeholder for the query expression.
    # return Query.run(data_frame_source, query_expresion)
    pass


class PragmaticNoise:
    """
    Drop rows or columns with missing data
    """

    def run(data_frame_source: DataFrameFederated, query_expresion: Any) -> DataFrameFederated:

        check_instance(data_frame_source, DataFrameFederated)
        # check_instance(query_expresion, list) #TODO
        data_frame_target = data_frame_source.create_new()
        for dataset_id in data_frame_source.dict_dataframe:
            data_frame_target.dict_dataframe[dataset_id] = PragmaticNoisePrecompute.run(
                data_frame_source.dict_dataframe[dataset_id], query_expresion
            )
        return data_frame_target
