from typing import List, Tuple

import numpy as np
from sail_core.tools_common import check_instance, sanitize_dict_for_json
from sail_safe_functions.aggregator.reference_series import ReferenceSeries
from sail_safe_functions.aggregator.service_reference import ServiceReference
from sail_safe_functions.aggregator.tools_common import check_empty_series, check_series_nan, check_series_one_value
from sail_safe_functions.safe_function_base import SafeFunctionBase


class MeanPrecompute(SafeFunctionBase):
    """
    Precomputes data for computing the mean
    """

    @staticmethod
    def run(
        reference_sample_0: ReferenceSeries,
    ) -> List:
        """
        Function to calculate the precomputes for mean

            :param reference_sample_0: sample input
            :type reference_sample_0: ReferenceSeries
            :return: precomputes of mean TODO: please be more verbose i.e "local mean to be aggregated." The parameter descriptions should add more information.
            :rtype: Tuple[ List[float], List[bool] ]
        """
        # there seems to be a problem here with this annotation
        check_instance(reference_sample_0, ReferenceSeries)

        sample_0 = ServiceReference.get_instance().reference_to_series(reference_sample_0)

        check_series_nan(sample_0)
        check_empty_series(sample_0)
        check_series_nan(sample_0)
        check_series_one_value(sample_0)
        sample_0 = sample_0.to_numpy()

        sum_x_0 = np.sum(sample_0).item()
        sample_0_degrees_of_freedom = len(sample_0)

        precompute = [sum_x_0, sample_0_degrees_of_freedom]
        precompute = sanitize_dict_for_json(precompute)
        return precompute
