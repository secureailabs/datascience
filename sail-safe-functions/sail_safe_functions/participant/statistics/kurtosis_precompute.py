from typing import List

import numpy as np
from sail_core.tools_common import check_instance, sanitize_dict_for_json
from sail_safe_functions.aggregator.reference_series import ReferenceSeries
from sail_safe_functions.aggregator.service_reference import ServiceReference
from sail_safe_functions.aggregator.tools_common import check_empty_series, check_series_nan, check_series_one_value
from sail_safe_functions.safe_function_base import SafeFunctionBase


class KurtosisPrecompute(SafeFunctionBase):

    """
    Precomputes data for Kurtosis
    """

    @staticmethod
    def run(sample_0_series: ReferenceSeries) -> List[float]:
        """Generates the geometric moments for use in a Kurtosis

        Parameters
        ----------
        sample_0_series : ReferenceSeries
            The series for sample_0
        Returns
        -------
        a list of 3 floats precomputes value
        """

        sample_0 = ServiceReference.get_instance().reference_to_series(sample_0_series).to_numpy()
        check_empty_series(sample_0)
        check_series_nan(sample_0)
        check_series_one_value(sample_0)

        # First
        sum_x_0 = np.sum(sample_0)
        # second
        sum_xx_0 = np.sum(sample_0 * sample_0)
        # Third
        sum_xxx_0 = np.sum(sample_0 * sample_0 * sample_0)
        # Fourth
        sum_xxxx_0 = np.sum(sample_0 * sample_0 * sample_0 * sample_0)
        # Sample size
        count_0 = len(sample_0)

        precompute = [sum_x_0, sum_xx_0, sum_xxx_0, sum_xxxx_0, count_0]
        precompute = sanitize_dict_for_json(precompute)
        return precompute
