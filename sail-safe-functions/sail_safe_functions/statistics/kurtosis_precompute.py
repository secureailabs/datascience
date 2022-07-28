from typing import List

import numpy as np
import pandas as pd


class KurtosisPrecompute:
    """
    Precomputes data for Kurtosis
    """

    def Run(sample_0_dataframe: pd.DataFrame) -> List[float]:
        """Generates the geometric moments for use in a Kurtosis

        Parameters
        ----------
        sample_0_dataframe : pd.DataFrame
            The dataframe for sample_0
        Returns
        -------
        a list of 3 floats precomputes value
        """

        sample_0 = sample_0_dataframe.to_numpy()
        # First
        sum_x_0 = np.sum(sample_0)
        # second
        sum_xx_0 = np.sum(sample_0 * sample_0)
        # Third
        sum_xxx_0 = np.sum(sample_0 * sample_0 * sample_0)
        # Fourth
        sum_xxxx_0 = np.sum(sample_0 * sample_0 * sample_0 * sample_0)
        # Sample size
        count_0 = len(sample_0)

        list_precompute = [sum_x_0, sum_xx_0, sum_xxx_0, sum_xxxx_0, count_0]

        return list_precompute
