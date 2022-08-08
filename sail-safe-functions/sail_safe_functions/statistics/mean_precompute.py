from typing import List, Tuple

import numpy as np
import pandas as pd


class MeanPrecompute:
    """
    Precomputes data for computing the mean
    """

    def run(
        sample_0_dataframe: pd.Series,
    ) -> Tuple[
        List[float], List[bool]
    ]:  # there seems to be a problem here with this annotation
        """
        function to calculate the precomputes for mean

        :param sample_0_dataframe: _description_
        :type sample_0_dataframe: pd.Series
        :return: _description_
        :rtype: Tuple[ List[float], List[bool] ]
        """
        sample_0 = sample_0_dataframe.to_numpy()

        sum_x_0 = np.sum(sample_0)
        sample_0_degrees_of_freedom = len(sample_0)

        list_precompute = [sum_x_0, sample_0_degrees_of_freedom]
        # list_safe = [False, False, False, False, False, False ]
        return list_precompute  # , list_safe
