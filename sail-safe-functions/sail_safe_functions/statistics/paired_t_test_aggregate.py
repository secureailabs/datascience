from typing import List, Tuple

import numpy as np
from sail_safe_functions.safe_function_base import SafeFunctionBase
from sail_safe_functions_orchestrator.tools_common import check_variance_zero



class PairedTTestAggregate(SafeFunctionBase):
    """
    Aggregates data for doing a paired t-test
    """

    def run(list_list_precompute: List[List[float]]) -> Tuple[float, float]:
        """collects the parts of a t-test and aggregates them into statisitcs

        :param list_list_precompute: a list of 3 floats; two moments for sample_d followed by the size of paired sample
        :type list_list_precompute: List[List[float]]
        :return: returns a t-statistic and its effect size
        :rtype: Tuple[float, float]
        """

        sum_d_0 = 0
        sum_dd_0 = 0
        size_sample_d = 0

        for list_precompute in list_list_precompute:
            sum_d_0 += list_precompute[0]
            sum_dd_0 += list_precompute[1]
            size_sample_d += list_precompute[2]

        sample_mean_d = sum_d_0 / size_sample_d
        sample_variance_d = ((sum_dd_0 / size_sample_d) - (sample_mean_d * sample_mean_d)) * (
            size_sample_d / (size_sample_d - 1)  # unbiased estimator (numpy version is biased by default)
        )
        check_variance_zero(sample_variance_d)
        t_statistic = sample_mean_d / (np.sqrt(sample_variance_d) / np.sqrt(size_sample_d))
        degrees_of_freedom = size_sample_d - 1

        # TODO we need to enable this when error handling is implemented
        # if degrees_of_freedom < 20:
        #     raise Exception()
        return t_statistic, degrees_of_freedom
