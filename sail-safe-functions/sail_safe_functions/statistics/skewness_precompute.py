from typing import List

import numpy as np
import pandas as pd


class SkewnessPrecompute:
    """
    Precomputes data for computing skewness
    """

    def run(sample_0_dataframe: pd.DataFrame) -> List[float]:
        """Generates the geometric moments for use in a Skewness

        Parameters
        ----------
        sample_0_dataframe : pd.DataFrame
            The dataframe for sample_0
        Returns
        -------
        a list of 3 floats precompute value
        """

        sample_0 = sample_0_dataframe.to_numpy()
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
