from typing import List

import pandas as pd
import numpy as np


class UnpairedTTestPrecompute(object):
    def __init__(self) -> None:
        super().__init__()

    def run(sample_0_series: pd.Series, sample_1_series: pd.Series) -> List[float]:
        """Generates the geometric moments for use in a T-Test

        Parameters
        ----------
        sample_0_series : pd.Series
            The series for sample_0

        sample_1_series : pd.Series
            The series for sample_1

        Returns
        -------
        a list of 6 floats, two moments for sample_0 followed by the size of sample_0 and two moments for sample_1 followed by the size of sample 1
        """
        sample_0 = sample_0_series.to_numpy()
        sample_1 = sample_1_series.to_numpy()

        sum_x_0 = np.sum(sample_0)
        sum_xx_0 = np.sum(sample_0 * sample_0)
        count_0 = len(sample_0)

        sum_x_1 = np.sum(sample_1)
        sum_xx_1 = np.sum(sample_1 * sample_1)
        count_1 = len(sample_1)

        list_precompute = [sum_x_0, sum_xx_0, count_0, sum_x_1, sum_xx_1, count_1]

        return list_precompute
