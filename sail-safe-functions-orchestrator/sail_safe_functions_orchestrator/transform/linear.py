from abc import abstractmethod
from typing import List

import numpy
from sail_safe_functions.transform.linear_precompute import LinearPrecompute
from sail_safe_functions_orchestrator.transform.transform_base import TransformBase
from sail_safe_functions_orchestrator.data_frame_federated import DataFrameFederated


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
    return LinearPrecompute.run(
        data_frame_source,
        array_input,
        list_name_feature_source,
        list_name_feature_target,
        inverse,
    )


class Linear(TransformBase):
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
        list_reference = []
        for dataset_id in data_frame_source.list_dataset_id:
            client = data_frame_source.service_client.get_client(dataset_id)
            reference_data_frame = data_frame_source.dict_reference_data_frame[dataset_id]
            list_reference.append(
                client.call(
                    LinearPrecompute,
                    reference_data_frame,
                    array_input,
                    list_name_feature_source,
                    list_name_feature_target,
                    inverse,
                )
            )
        return DataFrameFederated(
            data_frame_source.service_client, list_reference, data_frame_source.data_model_data_frame
        )

    #@abstractmethod
    def fit(self, data_frame: DataFrameFederated):
        raise NotImplementedError()

    def transform(self, data_frame: DataFrameFederated) -> DataFrameFederated:
        raise NotImplementedError()
