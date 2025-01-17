from typing import List

import numpy as np
from sail_core.tools_common import sanitize_dict_for_json
from sail_safe_functions.aggregator.reference_series import ReferenceSeries
from sail_safe_functions.aggregator.service_reference import ServiceReference
from sail_safe_functions.aggregator.tools_common import check_empty_series, check_series_nan, check_series_one_value
from sail_safe_functions.safe_function_base import SafeFunctionBase


class PairedTTestPrecompute(SafeFunctionBase):
    """
    Precomputes data for performing a paired t-test
    """

    @staticmethod
    def run(sample_0_series: ReferenceSeries, sample_1_series: ReferenceSeries) -> List[float]:
        """Generates the geometric moments for use in a T-Test

        :param sample_0_series:  The series for sample_0
        :type sample_0_series: ReferenceSeries
        :param sample_1_series: The series for sample_1
        :type sample_1_series: ReferenceSeries
        :return: a list of 3 floats, two moments for sample_d followed by the size of sample_d
        :rtype: List[float]
        """

        sample_0 = ServiceReference.get_instance().reference_to_series(sample_0_series).to_numpy()
        sample_1 = ServiceReference.get_instance().reference_to_series(sample_1_series).to_numpy()
        check_empty_series(sample_0)
        check_empty_series(sample_1)
        check_series_nan(sample_0)
        check_series_one_value(sample_0)
        check_series_nan(sample_1)
        check_series_one_value(sample_1)

        sample_d = sample_0 - sample_1
        sum_d_0 = np.sum(sample_d)
        sum_dd_0 = np.sum(sample_d * sample_d)
        count_d = len(sample_d)

        precompute = [sum_d_0, sum_dd_0, count_d]
        precompute = sanitize_dict_for_json(precompute)
        return precompute
