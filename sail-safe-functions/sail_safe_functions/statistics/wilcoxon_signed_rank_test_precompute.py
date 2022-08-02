from typing import List

import numpy
import pandas


class WilcoxonSignedRankTestPrecompute:
    """
    Precomputes data for the  WilcoxonSingedRankTest
    """

    def run(
        sample_difference: pandas.Series,
        sample_absolute_difference_ranked: pandas.Series,
    ):
        rank_minus = numpy.sum((sample_difference.to_numpy() < 0) * sample_absolute_difference_ranked.to_numpy())
        rank_plus = numpy.sum((sample_difference.to_numpy() > 0) * sample_absolute_difference_ranked.to_numpy())
        return [rank_minus, rank_plus]
