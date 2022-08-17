from abc import abstractmethod
from typing import List

import numpy
from sail_safe_functions_orchestrator import transform
from sail_safe_functions_orchestrator.data_frame_federated import DataFrameFederated
from sail_safe_functions_orchestrator.tools_common import check_instance
from sail_safe_functions_orchestrator.transform.transform_base import TransformBase


class Scaling(TransformBase):
    def __init__(self) -> None:
        self.list_add = None
        self.list_multiply = None

    @abstractmethod
    def fit(self, data_frame: DataFrameFederated, list_name_feature: List[str]) -> None:
        raise NotImplementedError()

    def transform(self, data_frame: DataFrameFederated) -> DataFrameFederated:
        check_instance(data_frame, DataFrameFederated)
        array_add = numpy.array(self.list_add)
        array_dot_product = numpy.zeros((len(self.list_add), len(self.list_add)))

        for i, multiply in enumerate(self.list_multiply):  # TODO this has a onliner
            array_dot_product[i, i] = multiply

        return transform.linear(
            data_frame, array_add, array_dot_product, self.list_name_feature, self.list_name_feature
        )
