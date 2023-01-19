from typing import List, Tuple

import numpy as np
import pandas as pd
from sail_core.tools_common import sanitize_dict_for_json
from sail_safe_functions.aggregator.reference_series import ReferenceSeries
from sail_safe_functions.aggregator.service_reference import ServiceReference
from sail_safe_functions.aggregator.tools_common import (
    check_empty_series,
    check_instance,
    check_series_nan,
    check_series_one_value,
)
from sail_safe_functions.safe_function_base import SafeFunctionBase


class VariancePrecompute(SafeFunctionBase):
    """
    Precomputes data for computing the variance
    """

    @staticmethod
    def run(
        sample_0_series: ReferenceSeries,
    ) -> List[float]:
        """
        Function collects the precomptues requireds for calculating variance

            :param sample_0_series: input series
            :type sample_0: ReferenceSeries
            :return: value of varaince
            :rtype: Tuple[ List[float], List[bool] ]
        """
        # there seems to be a problem here with this annotation -- Who wrote this??
        sample_0 = ServiceReference.get_instance().reference_to_series(sample_0_series).to_numpy()
        check_empty_series(sample_0)
        check_series_nan(sample_0)
        check_series_one_value(sample_0)
        sum_x_0 = np.sum(sample_0)
        sum_xx_0 = np.sum(sample_0 * sample_0)
        sample_0_dof = len(sample_0)

        precompute = [sum_x_0, sum_xx_0, sample_0_dof]
        precompute = sanitize_dict_for_json(precompute)
        return precompute
