from typing import List

import numpy as np
import pandas as pd


class PairedTTestPrecompute:
    """
    Precomputes data for performing a paired t-test
    """

    def run(sample_0_series: pd.Series, sample_1_series: pd.Series) -> List[float]:
        """Generates the geometric moments for use in a T-Test

        :param sample_0_series:  The series for sample_0
        :type sample_0_series: pd.Series
        :param sample_1_series: The series for sample_1
        :type sample_1_series: pd.Series
        :return: a list of 3 floats, two moments for sample_d followed by the size of sample_d
        :rtype: List[float]
        """

        sample_0 = sample_0_series.to_numpy()
        sample_1 = sample_1_series.to_numpy()
        sample_d = sample_0 - sample_1
        sum_d_0 = np.sum(sample_d)
        sum_dd_0 = np.sum(sample_d * sample_d)
        count_d = len(sample_d)

        list_precompute = [sum_d_0, sum_dd_0, count_d]

        return list_precompute
