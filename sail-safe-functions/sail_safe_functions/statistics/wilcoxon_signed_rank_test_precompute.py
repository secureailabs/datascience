import numpy
import pandas


class WilcoxonSingedRankTestPrecompute:
    """
    Precomputes data for the  WilcoxonSingedRankTest
    """

    def run(
        sample_difference: pandas.Series,
        sample_absolute_difference_ranked: pandas.Series,
    ):
        """
        Function to Precomputes data for the  WilcoxonSingedRankTest

            :param sample_difference: sample input
            :type sample_difference: pandas.Series
            :param sample_absolute_difference_ranked: absolute differences ranked
            :type sample_absolute_difference_ranked: pandas.Series
            :return: list rank_minus, rank_plus
            :rtype: list
        """
        rank_minus = numpy.sum((sample_difference.to_numpy() < 0) * sample_absolute_difference_ranked.to_numpy())
        rank_plus = numpy.sum((sample_difference.to_numpy() > 0) * sample_absolute_difference_ranked.to_numpy())
        return [rank_minus, rank_plus]
