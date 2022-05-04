import math
from typing import List, Tuple

import numpy as np


class UnpairedTTestAgregate:
    """
    Agregates data for doing a unpaired t-test (either the student t-test or the welch t-test)
    """

    def run(
        list_list_precompute: List[List[float]],
        equal_varriances: bool,
    ) -> Tuple[float, float]:
        """_summary_

        :param list_list_precompute: a list of lists of geometric moments and sample sizes
        :type list_list_precompute: List[List[float]]
        :param equal_varriances: assume equal variances,
        :type equal_varriances: bool, optional
        :return: A tuple of a t-statitic and a p-value
        :rtype: Tuple[float, float]
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
        sample_varriance_0 = ((sum_xx_0 / size_sample_0) - (sample_mean_0 * sample_mean_0)) * (
            size_sample_0 / (size_sample_0 - 1)  # unbiased estimator (numpy version is biased by default)
        )

        sample_mean_1 = sum_x_1 / size_sample_1
        sample_varriance_1 = ((sum_xx_1 / size_sample_1) - (sample_mean_1 * sample_mean_1)) * (
            size_sample_1 / (size_sample_1 - 1)  # unbiased estimator (np version is biased by default)
        )

        if equal_varriances:
            sample_varriance_pooled = (
                ((size_sample_0 - 1) * sample_varriance_0) + ((size_sample_1 - 1) * sample_varriance_1)
            ) / (size_sample_0 + size_sample_1 - 2)
            t_statistic = (sample_mean_0 - sample_mean_1) / (
                np.sqrt(sample_varriance_pooled) * np.sqrt((1 / size_sample_0 + 1 / size_sample_1))
            )
            degrees_of_freedom = size_sample_0 + size_sample_1 - 2

        else:
            t_statistic = (sample_mean_0 - sample_mean_1) / (
                np.sqrt((sample_varriance_0 / size_sample_0) + (sample_varriance_1 / size_sample_1))
            )
            # Welch–Satterthwaite equation:
            dof_nominator = math.pow(((sample_varriance_0 / size_sample_0) + (sample_varriance_1 / size_sample_1)), 2)
            dof_denominator = (
                math.pow(sample_varriance_0, 2) / (size_sample_0 * size_sample_0 * (size_sample_0 - 1))
            ) + (math.pow(sample_varriance_1, 2) / (size_sample_1 * size_sample_1 * (size_sample_1 - 1)))
            degrees_of_freedom = dof_nominator / dof_denominator

        # if degrees_of_freedom < 20:
        #     raise Exception()
        return t_statistic, degrees_of_freedom
