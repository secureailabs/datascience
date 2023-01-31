import math
from typing import List, Tuple

from sail_safe_functions.aggregator.series_federated import SeriesFederated
from sail_safe_functions.aggregator.statistics.estimator_one_sample import EstimatorOneSample
from sail_safe_functions.participant.statistics.skewness_precompute import SkewnessPrecompute
from scipy import stats


def skewness(
    sample_0: SeriesFederated,
) -> float:

    estimator = Skewness()
    return estimator.run(sample_0)


class Skewness(EstimatorOneSample):

    """
    An estimator for Skewness
    """

    def __init__(
        self,
    ) -> None:
        super().__init__("Skewness", ["skewness"])

    def run(
        self,
        sample_0: SeriesFederated,
    ) -> float:
        """
        It takes one federated series, and returns the skewness value of the series.

        :param sample_0: sample series
        :type sample_0: SeriesFederated
        :return: skewness value of series
        :rtype: float
        """
        list_precompute = sample_0.map_function(SkewnessPrecompute)

        skewness = self.aggregate(list_precompute)
        return skewness

    def aggregate(
        self,
        list_list_precompute: List[List[float]],
    ) -> float:

        """
        A Function to get the fedrated skewness value.
        same as scipy.skewsnes ()

        :param list_list_precompute: compute from different DF
        :type list_list_precompute: List[List[float]]
        :return: Skewness Value
        :rtype: Float

        """

        sum_x_0 = 0
        sum_xxx_0 = 0
        sum_xx_0 = 0
        size_sample_0 = 0
        # Combining precompute
        for list_precompute in list_list_precompute:
            sum_x_0 += list_precompute[0]
            sum_xx_0 += list_precompute[1]
            sum_xxx_0 += list_precompute[2]
            size_sample_0 += list_precompute[3]  # same as Count_0

        # Calculating sampel mean
        sample_mean_0 = sum_x_0 / size_sample_0
        # Calculating sample variance
        sample_variance_0 = (sum_xx_0 / size_sample_0) - (sample_mean_0 * sample_mean_0)
        # Calculating Sample
        sample_standard_deviation = math.sqrt(sample_variance_0)
        # mu3 Geometric
        mu3 = sum_xxx_0 / size_sample_0
        mean = sample_mean_0
        standard_deviation = sample_standard_deviation
        # Final Statistical formula for calculating skewness
        # wiki link below for the formula
        # https://en.wikipedia.org/wiki/Skewness
        skewness_value = (mu3 - (3 * mean * standard_deviation * standard_deviation) - mean**3) / (
            standard_deviation**3
        )

        return skewness_value

    def run_reference(self, sample_0: SeriesFederated):
        return stats.skew(sample_0.to_numpy())
