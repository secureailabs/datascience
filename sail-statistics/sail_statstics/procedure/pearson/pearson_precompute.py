import pandas as pd
from typing import List
import numpy as np


class PearsonPrecompute(object):
    def __init__(self) -> None:
        super().__init__()

    def run(sample_0_dataframe: pd.DataFrame, sample_1_dataframe: pd.DataFrame) -> List[float]:
        """
        Parameters
        ----------
        sample_0_dataframe : pd.DataFrame
            The dataframe for sample_0

        sample_1_dataframe : pd.DataFrame
            The dataframe for sample_1

        Returns
        -------
        a list of 3 floats
        """
        sample_0 = sample_0_dataframe.to_numpy()
        sample_1 = sample_1_dataframe.to_numpy()

        sum_x_0 = np.sum(sample_0)
        sum_xx_0 = np.sum(sample_0 * sample_0)
        sample_0_dof = len(sample_0)

        sum_x_1 = np.sum(sample_1)
        sum_xx_1 = np.sum(sample_1 * sample_1)
        sample_1_dof = len(sample_1)

        sum_x1_into_x2 = np.sum(np.multiply(sample_0, sample_1))

        list_precompute = [sum_x_0, sum_xx_0, sample_0_dof, sum_x_1, sum_xx_1, sample_1_dof, sum_x1_into_x2]
        print(list_precompute)

        # list_safe = [False, False, False, False, False, False ]
        return list_precompute  # , list_safe
