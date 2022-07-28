import math
from typing import List


class WilcoxonSingedRankTestAggregate:
    """
    Aggregates data for WilcoxonSingedRankTest
    """

    def Run(list_precompute: List):
        rank_minus = 0
        rank_plus = 0
        for precompute in list_precompute:
            rank_minus += precompute[0]
            rank_plus += precompute[1]
        return rank_minus, rank_plus
