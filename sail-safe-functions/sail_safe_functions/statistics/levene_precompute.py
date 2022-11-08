from typing import List, Tuple

import numpy as np
import pandas as pd
from sail_safe_functions_orchestrator.reference_series import ReferenceSeries
from sail_safe_functions_orchestrator.service_reference import ServiceReference
from sail_safe_functions_orchestrator.tools_common import (
    check_instance,
    check_series_nan,
    check_empty_series,
    check_series_one_value,
)


class LevenePrecompute:
    """
    Precomputes data for Levens Test
    """

    def run(
        reference_series_0: ReferenceSeries,
        reference_series_1: ReferenceSeries,
        mean_0: float,
        mean_1: float,
    ) -> Tuple[List[float], List[bool]]:  # there seems to be a problem here with this annotation
        """
        Precomputes data for Levens Test
        ----------
        sample_0_series : ReferenceSeries
            The series for sample_0

        sample_1_series : ReferenceSeries
            The series for sample_1

        Returns
        -------
        a list of 6 floats, two moments for sample_0 followed by the size of sample_0 and two moments for sample_1 followed by the size of sample 1

        """

        sample_0 = ServiceReference.get_instance().reference_to_series(reference_series_0).to_numpy()
        sample_1 = ServiceReference.get_instance().reference_to_series(reference_series_1).to_numpy()
        check_empty_series(sample_0)
        check_empty_series(sample_1)
        sum_x_0 = np.sum(sample_0)
        sum_xx_0 = np.sum(sample_0 * sample_0)
        count_0 = len(sample_0)

        sum_x_1 = np.sum(sample_1)
        sum_xx_1 = np.sum(sample_1 * sample_1)
        count_1 = len(sample_1)

        z1j = abs(sample_0 - mean_0)
        z2j = abs(sample_1 - mean_1)

        list_precompute = [
            sum_x_0,
            sum_xx_0,
            count_0,
            sum_x_1,
            sum_xx_1,
            count_1,
            z1j,
            z2j,
        ]

        return list_precompute
