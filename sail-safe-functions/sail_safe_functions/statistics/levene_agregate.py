from typing import List

import numpy as np


class LeveneAgregate:
    """
    Agregates data for doing a unpaired t-test (either the student t-test or the welch t-test)
    """

    def run(
        list_list_precompute: List[List[float]],
        equal_varriances: bool = False,
    ):
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

        denom_1 = final_z1j - z1_
        denom_1 = np.sum(denom_1 * denom_1)

        denom_2 = final_z2j - z2_
        denom_2 = np.sum(denom_2 * denom_2)

        final_denom = denom_1 + denom_2
        length1 = size_sample_0
        length2 = size_sample_1
        dof = length1 + length2 - 2
        final_nem = dof * (length1 * (z1_ - z__) * (z1_ - z__) + length2 * (z2_ - z__) * (z2_ - z__))

        f_statictic = final_nem / final_denom

        return f_statictic, dof