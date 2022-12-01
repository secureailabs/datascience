from typing import Tuple

import numpy as np
from sail_safe_functions.safe_function_base import SafeFunctionBase
from sail_safe_functions_orchestrator.reference_series import ReferenceSeries
from sail_safe_functions_orchestrator.service_reference import ServiceReference
from sail_safe_functions_orchestrator.tools_common import (
    check_empty_series,
    check_instance,
    check_series_nan,
    check_series_one_value,
)


class MinMaxPrecompute(SafeFunctionBase):
    """
    Precomputes min and max for a given sample
    """

    def run(sample_0_series: ReferenceSeries) -> Tuple[float, float]:
        """
        This function is designed to counteract disclosure of the min and max while giving them estimates that
        are independant for sample size bigger than 2. The function guarantees that min <= sample_min and sample_max <= max
        For uniform distributions this follows the UMVU-estimator altough with bigger variance
        For normal distribution this creates a min and a max that are far outside the sample
        min and max to protect outliers.
        TODO this function can be improved by doing the actual estimation in the aggregate section

        :param sample_0_series: the sample from witch to estimate the min and max
        :type sample_0_series: ReferenceSeries
        :raises ValueError: raises a ValueError if the series contains `na` values
        :return: The min and max estimate from the series
        :rtype: Tuple[float, float]
        """

        sample_0 = ServiceReference.get_instance().reference_to_series(sample_0_series).to_numpy()
        if np.isnan(np.sum(sample_0)):
            raise ValueError("Sample contains `na` values")
        sample_0 = np.sort(sample_0)
        check_empty_series(sample_0)
        check_series_nan(sample_0)
        check_series_one_value(sample_0)

        subsample_size = int(np.ceil(np.sqrt(sample_0.size)))
        subsample_min = sample_0[:subsample_size]
        subsample_max = sample_0[-subsample_size:]
        subsample_min_width = np.max(subsample_min) - np.min(subsample_min)
        estimate_min = np.min(subsample_min) - (subsample_min_width**2 / sample_0.size)
        subsample_max_width = np.max(subsample_max) - np.min(subsample_max)
        estimate_max = np.max(subsample_max) + (subsample_max_width**2 / sample_0.size)
        return estimate_min, estimate_max
