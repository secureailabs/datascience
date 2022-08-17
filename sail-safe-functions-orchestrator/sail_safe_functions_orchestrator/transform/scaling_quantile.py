from typing import List

import numpy
from sail_safe_functions_orchestrator import statistics
from sail_safe_functions_orchestrator.data_frame_federated import DataFrameFederated
from sail_safe_functions_orchestrator.tools_common import check_instance
from sail_safe_functions_orchestrator.transform.scaling import Scaling


class ScalingQuantile(Scaling):
    """ScalingQuantile transforms a dataframe with only numbers
    to a dataframe where all values are scaled between a lower and a upper quantile

    """

    def __init__(self, lower: float, upper: float) -> None:
        if lower < 0:
            raise ValueError("lower cannot be below 0")

        if 1 < upper:
            raise ValueError("upper cannot be above 1")

        if upper <= lower:
            raise ValueError("lower must be strickly smaller than upper")

        self.lower = lower
        self.upper = upper

    def fit(self, data_frame: DataFrameFederated, list_name_feature: List[str]):
        check_instance(data_frame, DataFrameFederated)
        self.list_name_feature = list_name_feature
        self.list_add = []
        self.list_multiply = []
        for name_feature in self.list_name_feature:
            if data_frame[name_feature].dtype != float:
                raise Exception("Can only scale features of type float")
            # TODO also check if it has at least 5 unique values spead over the domain
            list_quantile = statistics.quantiles(data_frame[name_feature], [self.lower, self.upper])
            self.list_add.append(-list_quantile[0])
            self.list_multiply.append(1 / (list_quantile[1] - list_quantile[0]))
