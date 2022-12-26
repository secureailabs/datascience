import math
from typing import List, Tuple

import numpy as np
from sail_safe_functions.aggregator.tools_common import check_variance_zero
from sail_safe_functions.safe_function_base import SafeFunctionBase


class WelchTTestAggregate(SafeFunctionBase):
    """
    Aggregates data for doing a unpaired t-test (either the student t-test or the welch t-test)
    """

    def run(
        list_list_precompute: List[List[float]],
    ) -> Tuple[float, float]:
        sum_x_0 = 0
        sum_xx_0 = 0
        size_sample_0 = 0
        sum_x_1 = 0
        sum_xx_1 = 0
        size_sample_1 = 0
        for list_precompute in list_list_precompute:
            sum_x_0 += list_precompute[0]
            sum_xx_0 += list_precompute[1]
            size_sample_0 += list_precompute[2]
            sum_x_1 += list_precompute[3]
            sum_xx_1 += list_precompute[4]
            size_sample_1 += list_precompute[5]

        sample_mean_0 = sum_x_0 / size_sample_0
        sample_variance_0 = ((sum_xx_0 / size_sample_0) - (sample_mean_0 * sample_mean_0)) * (
            size_sample_0 / (size_sample_0 - 1)  # unbiased estimator (numpy version is biased by default)
        )
        check_variance_zero(sample_variance_0)

        sample_mean_1 = sum_x_1 / size_sample_1
        sample_variance_1 = ((sum_xx_1 / size_sample_1) - (sample_mean_1 * sample_mean_1)) * (
            size_sample_1 / (size_sample_1 - 1)  # unbiased estimator (np version is biased by default)
        )
        check_variance_zero(sample_variance_1)
        t_statistic = (sample_mean_0 - sample_mean_1) / (
            np.sqrt((sample_variance_0 / size_sample_0) + (sample_variance_1 / size_sample_1))
        )
        # Welch–Satterthwaite equation:
        degrees_of_freedom_numerator = math.pow(
            ((sample_variance_0 / size_sample_0) + (sample_variance_1 / size_sample_1)),
            2,
        )
        degrees_of_freedom_denominator = (
            math.pow(sample_variance_0, 2) / (size_sample_0 * size_sample_0 * (size_sample_0 - 1))
        ) + (math.pow(sample_variance_1, 2) / (size_sample_1 * size_sample_1 * (size_sample_1 - 1)))
        degrees_of_freedom = degrees_of_freedom_numerator / degrees_of_freedom_denominator

        return t_statistic, degrees_of_freedom
