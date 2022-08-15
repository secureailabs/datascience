from sail_safe_functions_orchestrator.transform.scaling_quantile import ScalingQuantile


class ScalingMinMax(ScalingQuantile):
    def __init__(self) -> None:
        super().__init__(0, 1)
