from abc import abstractmethod
from typing import List

import numpy
from sail_safe_functions.transform.expression_precompute import ExpresionPrecompute
from sail_safe_functions_orchestrator.data_frame_federated import DataFrameFederated


def convert_expresion(
    data_frame_source: DataFrameFederated, name_feature_source: str, name_feature_target: str, expresion_string: str
):
    # TODO this thing is suuuuuuper dangerous. It is basically arbitrary code execution as a service
    data_frame_target = data_frame_source.create_new()
    for dataset_id in data_frame_source.dict_dataframe:
        data_frame_target.dict_dataframe[dataset_id] = ExpresionPrecompute.run(
            data_frame_source.dict_dataframe[dataset_id], name_feature_source, name_feature_target, expresion_string
        )
    return data_frame_target
