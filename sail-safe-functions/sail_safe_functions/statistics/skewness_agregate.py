from typing import List
import math


class SkewnessAgregate(object):
    def __init__(self) -> None:
        super().__init__()

    def run(list_list_precompute: List[List[float]]):

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
        # Calculating sample varriance
        sample_varriance_0 = (sum_xx_0 / size_sample_0) - (sample_mean_0 * sample_mean_0)
        # Calculating Sample
        sample_standard_deviation = math.sqrt(sample_varriance_0)
        # mu3 Geometric
        mu3 = sum_xxx_0 / size_sample_0
        mean = sample_mean_0
        sd = sample_standard_deviation
        # Final Statistical formula for calculating skewness
        # wiki link below for the formula
        # https://en.wikipedia.org/wiki/Skewness
        skewness_value = (mu3 - (3 * mean * sd * sd) - mean**3) / (sd**3)

        return skewness_value
