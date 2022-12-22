from abc import abstractmethod
from typing import List

import numpy
from sail_safe_functions_orchestrator import transform
from sail_safe_functions_orchestrator.data_frame_federated import DataFrameFederated
from sail_safe_functions_orchestrator.tools_common import check_instance
from sail_safe_functions_orchestrator.transform.linear import Linear
from sail_safe_functions_orchestrator.transform.transform_base import TransformBase


class Scaling(TransformBase):
    @staticmethod
    def run(
        data_frame: DataFrameFederated,
        array_input,
        list_name_feature_source,
        list_name_feature_target,
        inverse,
    ):

        return transform.Linear(data_frame, array_input, list_name_feature_source, list_name_feature_target, inverse)
