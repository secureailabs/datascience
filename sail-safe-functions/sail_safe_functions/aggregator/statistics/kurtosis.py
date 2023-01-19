import math
from typing import List, Tuple

from sail_safe_functions.aggregator.series_federated import SeriesFederated
from sail_safe_functions.aggregator.statistics.estimator import Estimator
from sail_safe_functions.participant.statistics.kurtosis_precompute import KurtosisPrecompute
from scipy import stats


def kurtosis(sample_0: SeriesFederated) -> Tuple[float]:
    """
    Perform federated kurtosis.
    It takes one federated series, and returns the kurtosis value of the series

    :param sample_0: sample series
    :type sample_0: SeriesFederated
    :return: Kurtosis value
    :rtype: Tuple[float]
    """
    estimator = Kurtosis()
    return estimator.run(sample_0)


class Kurtosis(Estimator):
    """
    A estimator for Kurtosis
    """

    def __init__(self) -> None:
        super().__init__(["kurtosis"])

    def run(self, sample_0: SeriesFederated):
        # Calculating precompute
        list_precompute = sample_0.map_function(KurtosisPrecompute)
        kurtosis_value = self.aggregate(list_precompute)
        return kurtosis_value

    def aggregate(self, list_list_precompute: List[List[float]]) -> float:

        """
        A Function to get the fedrated Kurtosis value.
        same as scipy.skewsnes ()

        :param list_list_precompute: compute from different DF
        :type list_list_precompute: List[List[float]]
        :return: Kurtosis Value
        :rtype: Float

        """

        sum_x_0 = 0
        sum_xx_0 = 0
        sum_xxx_0 = 0
        sum_xxxx_0 = 0
        size_sample_0 = 0
        # Combining precompute
        for list_precompute in list_list_precompute:
            sum_x_0 += list_precompute[0]
            sum_xx_0 += list_precompute[1]
            sum_xxx_0 += list_precompute[2]
            sum_xxxx_0 += list_precompute[3]
            size_sample_0 += list_precompute[4]  # same as Count_0

        # Calculating sampel mean
        sample_mean_0 = sum_x_0 / size_sample_0
        # Calculating sample variance
        sample_variance_0 = (sum_xx_0 / size_sample_0) - (sample_mean_0 * sample_mean_0)
        # Calculating Sample
        sample_standard_deviation = math.sqrt(sample_variance_0)

        # mu Geometric
        mu2 = sum_xx_0 / size_sample_0
        mu3 = sum_xxx_0 / size_sample_0
        mu4 = sum_xxxx_0 / size_sample_0
        mean = sample_mean_0
        standard_deviation = sample_standard_deviation

        # Final Statistical formula for calculating Kurtosis
        # wiki link below for the formula
        # https://en.wikipedia.org/wiki/Kurtosis

        kurtosis_value = ((mu4) - 3 * (mean**4) - 4 * ((mu3) * (mean)) + 6 * ((mu2) * (mean**2))) / (
            standard_deviation**4
        )

        return kurtosis_value - 3

    def run_reference(self, sample_0: SeriesFederated):
        return stats.kurtosis(sample_0.to_numpy())
