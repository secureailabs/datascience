from typing import List
from sail_safe_functions.safe_function_base import SafeFunctionBase


class KolmogorovSmirnovTestAggregate(SafeFunctionBase):
    """
    Aggregates data for the KolmogorovSmirnov test
    """

    def run(list_precompute: List[float]) -> float:
        list_max = []
        for precompute in list_precompute:
            list_max.append(precompute)

        return max(list_max)
