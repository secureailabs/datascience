from typing import List

import numpy as np
import pandas as pd
from sail_safe_functions_orchestrator.reference_series import ReferenceSeries
from sail_safe_functions_orchestrator.service_reference import ServiceReference


class UnpairedTTestPrecompute:
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

        sum_x_0 = np.sum(sample_0)
        sum_xx_0 = np.sum(sample_0 * sample_0)
        count_0 = len(sample_0)

        sum_x_1 = np.sum(sample_1)
        sum_xx_1 = np.sum(sample_1 * sample_1)
        count_1 = len(sample_1)

        list_precompute = [sum_x_0, sum_xx_0, count_0, sum_x_1, sum_xx_1, count_1]

        return list_precompute
