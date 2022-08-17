from abc import abstractmethod
from typing import List

import numpy
from sail_safe_functions.transform.linear_precompute import LinearPrecompute
from sail_safe_functions_orchestrator.data_frame_federated import DataFrameFederated
from sail_safe_functions_orchestrator.transform.transform_base import TransformBase


def linear(
    data_frame_source: DataFrameFederated,
    array_add: numpy.ndarray,
    array_dot_product: numpy.ndarray,
    list_name_feature_source: List[str],
    list_name_feature_target: List[str],
):
    # TODO add the augmentation vector to make this more flexibel and get rid of an argument
    data_frame_target = data_frame_source.create_new()
    for dataset_id in data_frame_source.dict_dataframe:
        data_frame_target.dict_dataframe[dataset_id] = LinearPrecompute.run(
            data_frame_source.dict_dataframe[dataset_id],
            array_add,
            array_dot_product,
            list_name_feature_source,
            list_name_feature_target,
        )
    return data_frame_target


class Linear(TransformBase):
    def __init__(self) -> None:
        self.array_transfrom = None

    @abstractmethod
    def fit(self, data_frame: DataFrameFederated):
        raise NotImplementedError()

    def transform(self, data_frame: DataFrameFederated) -> DataFrameFederated:
        raise NotImplementedError()
