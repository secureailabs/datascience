from abc import abstractmethod
from typing import List

import numpy
from sail_safe_functions.aggregator.data_frame_federated import DataFrameFederated
from sail_safe_functions.participant.transform.linear_precompute import LinearPrecompute


def linear(
    data_frame_source: DataFrameFederated,
    array_input: numpy.ndarray,
    list_name_feature_source: List[str],
    list_name_feature_target: List[str],
    inverse: bool,
):
    """
    Perform the Federated linear transform

    :param data_frame_source: Data frame
    :type data_frame_source: DataFrameFederated
    :param array: contains two things 1. array_add and 2. array_dot product
    :type array: numpy.ndarray
    :param list_name_feature_source: feature you want to do linear transform
    :type list_name_feature_source: List[str]
    :param list_name_feature_target: new feature name after transformation
    :type list_name_feature_target: List[str]
    :param inverse: To do inverse linear transform
    :type inverse: bool
    :return: dataframe
    :rtype: dataframe
    """
    return Linear.run(
        data_frame_source,
        array_input,
        list_name_feature_source,
        list_name_feature_target,
        inverse,
    )


class Linear:
    def __init__(self) -> None:
        self.array_transfrom = None

    @staticmethod
    def run(
        data_frame_source: DataFrameFederated,
        array_input: numpy.ndarray,
        list_name_feature_source: List[str],
        list_name_feature_target: List[str],
        inverse: bool,
    ):
        list_reference = data_frame_source.map_function(
            LinearPrecompute,
            array_input,
            list_name_feature_source,
            list_name_feature_target,
            inverse,
        )
        return DataFrameFederated(list_reference, list_reference[0].data_model_data_frame)
