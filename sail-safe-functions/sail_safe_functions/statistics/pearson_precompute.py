from typing import List

import numpy as np
import pandas as pd


class PearsonPrecompute(object):
    """
    This class it get the precomputes required for the pearson

    :param object:
    :type object:
    """

    def Run(
        sample_0_dataframe: pd.DataFrame, sample_1_dataframe: pd.DataFrame
    ) -> List[float]:
        """
        Parameters
        ----------
        sample_0_dataframe : pd.DataFrame
            The dataframe for sample_0

        sample_1_dataframe : pd.DataFrame
            The dataframe for sample_1

        Returns
        -------
        a list of 6 floats
        """
        sample_0 = sample_0_dataframe.to_numpy()
        sample_1 = sample_1_dataframe.to_numpy()

        sum_x_0 = np.sum(sample_0)
        sum_xx_0 = np.sum(sample_0 * sample_0)
        sample_0_degrees_of_freedom = len(sample_0)

        sum_x_1 = np.sum(sample_1)
        sum_xx_1 = np.sum(sample_1 * sample_1)
        sample_1_degrees_of_freedom = len(sample_1)

        sum_x1_into_x2 = np.sum(np.multiply(sample_0, sample_1))

        list_precompute = [
            sum_x_0,
            sum_xx_0,
            sample_0_degrees_of_freedom,
            sum_x_1,
            sum_xx_1,
            sample_1_degrees_of_freedom,
            sum_x1_into_x2,
        ]

        # list_safe = [False, False, False, False, False, False ]
        return list_precompute  # , list_safe
