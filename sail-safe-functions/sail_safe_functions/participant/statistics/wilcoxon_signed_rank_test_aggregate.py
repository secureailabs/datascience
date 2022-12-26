from typing import List, Tuple
from sail_safe_functions.safe_function_base import SafeFunctionBase


class WilcoxonSingedRankTestAggregate(SafeFunctionBase):
    """
    Aggregates data for WilcoxonSingedRankTest
    """

    def run(list_precompute: List) -> Tuple[float, float]:
        rank_minus = 0
        rank_plus = 0
        for precompute in list_precompute:
            rank_minus += precompute[0]
            rank_plus += precompute[1]
        return rank_minus, rank_plus
