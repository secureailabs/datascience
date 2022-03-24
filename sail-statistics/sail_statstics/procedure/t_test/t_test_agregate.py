from typing import List

import numpy as np


class TTestAgregate(object):
    def __init__(self) -> None:
        super().__init__()

    def run(list_list_precompute: List[List[float]]):
        sum_x_0 = 0
        sum_xx_0 = 0
        dof_0 = 0
        sum_x_1 = 0
        sum_xx_1 = 0
        dof_1 = 0
        for list_precompute in list_list_precompute:
            sum_x_0 += list_precompute[0]
            sum_xx_0 += list_precompute[1]
            dof_0 += list_precompute[2]
            sum_x_1 += list_precompute[3]
            sum_xx_1 += list_precompute[4]
            dof_1 += list_precompute[5]

        sample_mean_0 = sum_x_0 / dof_0
        sample_varriance_0 = ((sum_xx_0 / dof_0) - (sample_mean_0 * sample_mean_0)) * (
            dof_0 / (dof_0 - 1)  # unbiased estimator (np version is biased by default)
        )

        sample_mean_1 = sum_x_1 / dof_1
        sample_varriance_1 = ((sum_xx_1 / dof_1) - (sample_mean_1 * sample_mean_1)) * (
            dof_1 / (dof_1 - 1)  # unbiased estimator (np version is biased by default)
        )

        sample_varriance_pooled = (((dof_0 - 1) * sample_varriance_0) + ((dof_1 - 1) * sample_varriance_1)) / (
            dof_0 + dof_1 - 2
        )
        t_statistic = (sample_mean_0 - sample_mean_1) / (
            np.sqrt(sample_varriance_pooled) * np.sqrt((1 / dof_0 + 1 / dof_1))
        )
        degrees_of_freedom = dof_0 + dof_1 - 2

        # TODO
        # if degrees_of_freedom < 20:
        #     raise Exception()
        return t_statistic, degrees_of_freedom
