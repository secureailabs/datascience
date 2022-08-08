from typing import List


class WilcoxonSingedRankTestAggregate:
    """
    Aggregates data for WilcoxonSingedRankTest
    """

    def run(list_precompute: List):
        """
        function Aggregates data for WilcoxonSingedRankTest

        :param list_precompute: _description_
        :type list_precompute: List
        :return: _description_
        :rtype: _type_
        """
        rank_minus = 0
        rank_plus = 0
        for precompute in list_precompute:
            rank_minus += precompute[0]
            rank_plus += precompute[1]
        return rank_minus, rank_plus
