from typing import List, Tuple

import numpy as np
import pandas as pd


class LevenePrecompute:
    """
    Precomputes data for computing the variance
    """

    def Run(
        sample_0_series: pd.Series,
        sample_1_series: pd.Series,
        mean_0: float,
        mean_1: float,
    ) -> Tuple[
        List[float], List[bool]
    ]:  # there seems to be a problem here with this annotation
        """
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
