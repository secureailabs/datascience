from typing import List

import numpy as np
from sail_core.tools_common import sanitize_dict_for_json
from sail_safe_functions.aggregator.reference_series import ReferenceSeries
from sail_safe_functions.aggregator.service_reference import ServiceReference
from sail_safe_functions.aggregator.tools_common import check_empty_series, check_series_nan, check_series_one_value
from sail_safe_functions.safe_function_base import SafeFunctionBase


class PearsonPrecompute(SafeFunctionBase):
    """
    This class it get the precomputes required for the pearson

    :param object:
    :type object:
    """

    @staticmethod
    def run(
        sample_0_series: ReferenceSeries,
        sample_1_series: ReferenceSeries,
    ) -> List[float]:
        """
        Parameters
        ----------
        sample_0_reference : ReferenceSeries
            The dataframe for sample_0

        sample_1_reference : ReferenceSeries
            The dataframe for sample_1

        Returns
        -------
        a list of 6 floats
        """
        sample_0 = ServiceReference.get_instance().reference_to_series(sample_0_series).to_numpy()
        sample_1 = ServiceReference.get_instance().reference_to_series(sample_1_series).to_numpy()
        check_empty_series(sample_0)
        check_empty_series(sample_1)
        check_series_nan(sample_0)
        check_series_one_value(sample_0)
        check_series_nan(sample_1)
        check_series_one_value(sample_1)

        sum_x_0 = np.sum(sample_0)
        sum_xx_0 = np.sum(sample_0 * sample_0)
        sample_0_degrees_of_freedom = len(sample_0)

        sum_x_1 = np.sum(sample_1)
        sum_xx_1 = np.sum(sample_1 * sample_1)
        sample_1_degrees_of_freedom = len(sample_1)

        sum_x1_into_x2 = np.sum(np.multiply(sample_0, sample_1))

        precompute = [
            sum_x_0,
            sum_xx_0,
            sample_0_degrees_of_freedom,
            sum_x_1,
            sum_xx_1,
            sample_1_degrees_of_freedom,
            sum_x1_into_x2,
        ]

        precompute = sanitize_dict_for_json(precompute)
        return precompute
