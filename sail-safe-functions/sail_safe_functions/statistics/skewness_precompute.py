from typing import List

import numpy as np
from sail_safe_functions_orchestrator.reference_series import ReferenceSeries
from sail_safe_functions_orchestrator.service_reference import ServiceReference
from sail_safe_functions.safe_function_base import SafeFunctionBase


class SkewnessPrecompute(SafeFunctionBase):
    """
    Precomputes data for computing skewness
    """

    def run(sample_0_series: ReferenceSeries) -> List[float]:
        """Generates the geometric moments for use in a Skewness

        Parameters
        ----------
        sample_0_series : ReferenceSeries
            The reference to the series for sample_0
        Returns
        -------
        a list of 3 floats precompute value
        """

        sample_0 = ServiceReference.get_instance().reference_to_series(sample_0_series).to_numpy()
        # First
        sum_x_0 = np.sum(sample_0)
        # second
        sum_xx_0 = np.sum(sample_0 * sample_0)
        # Third
        sum_xxx_0 = np.sum(sample_0 * sample_0 * sample_0)
        # Sample size
        count_0 = len(sample_0)

        list_precompute = [sum_x_0, sum_xx_0, sum_xxx_0, count_0]

        return list_precompute
