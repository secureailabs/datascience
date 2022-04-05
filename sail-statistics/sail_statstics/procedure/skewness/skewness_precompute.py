from typing import Any, List, Tuple

import pandas as pd
import numpy as np


class SkewnessPrecompute(object):
    def __init__(self) -> None:
        super().__init__()

    def run(sample_0_dataframe: pd.DataFrame) -> List[float]:
        """Generates the geometric moments for use in a Skewness

        Parameters
        ----------
        sample_0_dataframe : pd.DataFrame
            The dataframe for sample_0


        Returns
        -------
        a list of 3 floats
        """

        sample_0 = sample_0_dataframe.to_numpy()
        sum_x_0 = np.sum(sample_0)
        sum_xx_0 = np.sum(sample_0*sample_0)
        sum_xxx_0 = np.sum(sample_0 * sample_0*sample_0)
        count_0 = len(sample_0)

        list_precompute = [sum_x_0, sum_xx_0, sum_xxx_0, count_0]

        return list_precompute