from sail_safe_functions_orchestrator import statistics
from sail_safe_functions_orchestrator.data_frame_federated import DataFrameFederated
from sail_safe_functions_orchestrator.transform.transform_base import TransformBase


class ScalingQuantile(TransformBase):
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

    def fit(self, data_frame: DataFrameFederated):
        list_quantile = statistics.quantiles([self.lower, self.upper])
        self.add = -list_quantile[0]
        self.multipy = 1 / (list_quantile[1] - list_quantile[0])
