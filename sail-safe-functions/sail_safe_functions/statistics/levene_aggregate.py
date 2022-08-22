from typing import List

import numpy as np


class LeveneAggregate:
    """
    Aggregates data for Levens Test
    """

    def run(
        list_list_precompute: List[List[float]],
        equal_variances: bool = False,
    ):
        """
         Aggregates data for Levens Test

        :param list_list_precompute:  list of precompute
        :type list_list_precompute: List[List[float]]
        :param equal_variances: Applying for equal varaince or not, defaults to False
        :type equal_variances: bool, optional
        :return: _description_
        :rtype: _type_
        """
        sum_x_0 = 0
        sum_xx_0 = 0
        size_sample_0 = 0
        sum_x_1 = 0
        sum_xx_1 = 0
        size_sample_1 = 0
        final_z1j = []
        final_z2j = []
        for list_precompute in list_list_precompute:
            sum_x_0 += list_precompute[0]
            sum_xx_0 += list_precompute[1]
            size_sample_0 += list_precompute[2]
            sum_x_1 += list_precompute[3]
            sum_xx_1 += list_precompute[4]
            size_sample_1 += list_precompute[5]
            final_z1j.extend(list_precompute[6])
            final_z2j.extend(list_precompute[7])

        z1_ = np.mean(final_z1j)
        z2_ = np.mean(final_z2j)

        z__ = (z1_ + z2_) / 2

        denomenator_1 = final_z1j - z1_
        denomenator_1 = np.sum(denomenator_1 * denomenator_1)

        denomenator_2 = final_z2j - z2_
        denomenator_2 = np.sum(denomenator_2 * denomenator_2)

        final_denomenator = denomenator_1 + denomenator_2
        length1 = size_sample_0
        length2 = size_sample_1
        dof = length1 + length2 - 2
        final_numerator = dof * (length1 * (z1_ - z__) * (z1_ - z__) + length2 * (z2_ - z__) * (z2_ - z__))

        f_statictic = final_numerator / final_denomenator

        return f_statictic, dof
