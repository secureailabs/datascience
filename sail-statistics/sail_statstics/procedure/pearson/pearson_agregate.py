from typing import List
import math


class PearsonAgregate(object):
    def __init__(self) -> None:
        super().__init__()

    def run(list_list_precompute: List[List[float]]):
        sum_x_0 = 0
        sum_x_1 = 0
        sum_xx_0 = 0
        sum_xx_1 = 0
        sum_x1_into_x2 = 1
        size_sample_0 = 0
        size_sample_1 = 0
        for list_precompute in list_list_precompute:
            sum_x_0 += list_precompute[0]
            sum_xx_0 += list_precompute[1]
            size_sample_0 += list_precompute[2]
            sum_x_1 += list_precompute[3]
            sum_xx_1 += list_precompute[4]
            size_sample_1 += list_precompute[5]
            sum_x1_into_x2 *= list_precompute[6]

        # Calculating for the first column
        # Calculating sampel mean
        sample_mean_0 = sum_x_0 / size_sample_0
        # Calculating sample varriance
        sample_varriance_0 = (sum_xx_0 / size_sample_0) - (sample_mean_0 * sample_mean_0)
        # Calculating Sample
        sample_standard_deviation_0 = math.sqrt(sample_varriance_0)

        # Calculating for the second column
        # Calculating sampel mean
        sample_mean_1 = sum_x_1 / size_sample_1
        # Calculating sample varriance
        sample_varriance_1 = (sum_xx_1 / size_sample_1) - (sample_mean_1 * sample_mean_1)
        # Calculating Sample
        sample_standard_deviation_1 = math.sqrt(sample_varriance_1)

        E_xy = sum_x1_into_x2 / size_sample_0

        r = (E_xy - (sample_mean_0 * sample_mean_1)) / (sample_standard_deviation_0 * sample_standard_deviation_1)

        return r
