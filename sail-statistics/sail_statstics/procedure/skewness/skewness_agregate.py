from typing import List

import numpy as np
import math


class SkewnessAgregate(object):
    def __init__(self) -> None:
        super().__init__()

    def run(list_list_precompute: List[List[float]]):
        sum_x_0 = 0
        sum_xxx_0 = 0
        sum_xx_0 = 0
        size_sample_0 = 0
        print(list_list_precompute)
        for list_precompute in list_list_precompute:
            sum_x_0 += list_precompute[0]
            sum_xx_0 += list_precompute[1]
            sum_xxx_0 += list_precompute[2]
            size_sample_0 += list_precompute[3]  # Count_0

        sample_mean_0 = sum_x_0 / size_sample_0
        sample_varriance_0 = (sum_xx_0 / size_sample_0) - (sample_mean_0 * sample_mean_0)

        sample_standard_deviation = math.sqrt(sample_varriance_0)
        print(sample_standard_deviation)
        print(sample_mean_0)
        mu3 = sum_xxx_0 / size_sample_0
        print(mu3)
        mean = sample_mean_0
        sd = sample_standard_deviation
        skewness_value = (mu3 - (3 * mean * sd * sd) - mean**3) / (sd**3)

        return skewness_value
