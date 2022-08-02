import math
from typing import List


class WilcoxonSignedRankTestAggregate:
    """
    Aggregates data for WilcoxonSingedRankTest
    """

    def run(list_precompute: List):
        rank_minus = 0
        rank_plus = 0
        for precompute in list_precompute:
            rank_minus += precompute[0]
            rank_plus += precompute[1]
        return rank_minus, rank_plus
