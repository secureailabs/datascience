from typing import List
import math


class KurtosisAgregate(object):
    def __init__(self) -> None:
        super().__init__()

    def run(list_list_precompute: List[List[float]]):

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
        # Calculating sample varriance
        sample_varriance_0 = (sum_xx_0 / size_sample_0) - (sample_mean_0 * sample_mean_0)
        # Calculating Sample
        sample_standard_deviation = math.sqrt(sample_varriance_0)

        # mu Geometric
        mu2 = sum_xx_0 / size_sample_0
        mu3 = sum_xxx_0 / size_sample_0
        mu4 = sum_xxxx_0 / size_sample_0
        mean = sample_mean_0
        sd = sample_standard_deviation

        # Final Statistical formula for calculating Kurtosis
        # wiki link below for the formula
        # https://en.wikipedia.org/wiki/Kurtosis

        Kurtosis_value = ((mu4) - 3 * (mean**4) - 4 * ((mu3) * (mean)) + 6 * ((mu2) * (mean**2))) / (sd**4)

        return Kurtosis_value - 3
