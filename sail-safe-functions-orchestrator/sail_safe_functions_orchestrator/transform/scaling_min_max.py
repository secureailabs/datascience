import numpy
from sail_safe_functions_orchestrator import transform
from sail_safe_functions_orchestrator.data_frame_federated import DataFrameFederated
from sail_safe_functions_orchestrator.transform.scaling_quantile import ScalingQuantile


class ScalingMinMax(ScalingQuantile):
    def __init__(self) -> None:
        super().__init__(0, 1)
