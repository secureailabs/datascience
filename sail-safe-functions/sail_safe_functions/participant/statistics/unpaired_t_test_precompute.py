from typing import List

import numpy as np
from sail_core.tools_common import sanitize_dict_for_json
from sail_safe_functions.aggregator.reference_series import ReferenceSeries
from sail_safe_functions.aggregator.service_reference import ServiceReference
from sail_safe_functions.aggregator.tools_common import check_empty_series, check_series_nan, check_series_one_value
from sail_safe_functions.safe_function_base import SafeFunctionBase


class UnpairedTTestPrecompute(SafeFunctionBase):
    """
    Precomputes data for performing a unpaired t-test
    """

    def run(sample_0_series: ReferenceSeries, sample_1_series: ReferenceSeries) -> List[float]:
        """Generates the geometric moments for use in a T-Test

        Parameters
        ----------
        sample_0_series : ReferenceSeries
            The series for sample_0

        sample_1_series : ReferenceSeries
            The series for sample_1

        Returns
        -------
        a list of 6 floats, two moments for sample_0 followed by the size of sample_0 and two moments for sample_1 followed by the size of sample 1
        """
        sample_0 = ServiceReference.get_instance().reference_to_series(sample_0_series).to_numpy()
        sample_1 = ServiceReference.get_instance().reference_to_series(sample_1_series).to_numpy()
        check_empty_series(sample_0)
        check_empty_series(sample_1)
        check_series_nan(sample_0)
        # check_series_one_value(sample_0) #TODO these should be one level up
        check_series_nan(sample_1)
        # check_series_one_value(sample_1)

        sum_x_0 = np.sum(sample_0)
        sum_xx_0 = np.sum(sample_0 * sample_0)
        count_0 = len(sample_0)

        sum_x_1 = np.sum(sample_1)
        sum_xx_1 = np.sum(sample_1 * sample_1)
        count_1 = len(sample_1)

        precompute = [sum_x_0, sum_xx_0, count_0, sum_x_1, sum_xx_1, count_1]
        precompute = sanitize_dict_for_json(precompute)
        return precompute
