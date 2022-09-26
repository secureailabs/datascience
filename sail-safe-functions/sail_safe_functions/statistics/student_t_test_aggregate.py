import math
from typing import List

import numpy as np


class StudentTTestAggregate:
    """
    Aggregates data for doing a unpaired t-test (either the student t-test or the welch t-test)
    """

    def run(
        list_list_precompute: List[List[float]],
    ):
        """
        Function to run Aggregates data for doing a unpaired t-test
        (either the student t-test or the welch t-test)

            :param list_list_precompute: _description_
            :type list_list_precompute: List[List[float]]
            :return: _description_
            :rtype: float, int
        """
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

        sample_mean_1 = sum_x_1 / size_sample_1
        sample_variance_1 = ((sum_xx_1 / size_sample_1) - (sample_mean_1 * sample_mean_1)) * (
            size_sample_1 / (size_sample_1 - 1)  # unbiased estimator (np version is biased by default)
        )

        sample_variance_pooled = (
            ((size_sample_0 - 1) * sample_variance_0) + ((size_sample_1 - 1) * sample_variance_1)
        ) / (size_sample_0 + size_sample_1 - 2)
        t_statistic = (sample_mean_0 - sample_mean_1) / (
            np.sqrt(sample_variance_pooled) * np.sqrt((1 / size_sample_0 + 1 / size_sample_1))
        )
        degrees_of_freedom = size_sample_0 + size_sample_1 - 2

        return t_statistic, degrees_of_freedom
