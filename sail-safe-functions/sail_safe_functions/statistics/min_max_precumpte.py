from typing import Tuple

import numpy as np
import pandas as pd


class MinMaxPrecompute:
    """
    Precomputes min and max for a given sample
    """

    def run(series_sample: pd.Series) -> Tuple[float, float]:
        """This function is designed to counteract disclosure of the min and max while giving them estimates that
        are independant for sample size bigger than 2. The function guarantees that min <= sample_min and sample_max <= max
        For uniform distributions this follows the UMVUE altough with bigger varriance
        For normal distribution this creates a min and a max that are far outside the sample
        min and max to protect outliers.
        TODO this function can be improved by doing the actual estimation in the agregate section

        :param series_sample: _description_
        :type series_sample: pd.Series
        :raises ValueError: raises a ValueError if the series contains `na` values
        :return: The min and max estimate from the series
        :rtype: Tuple[float, float]
        """
        if 0 < series_sample.isna().sum():
            raise ValueError("Sample contains `na` values")
        array_sample = np.array(series_sample.sort_values(ascending=True, inplace=False))
        subsample_size = int(np.ceil(np.sqrt(series_sample.size)))
        subsample_min = array_sample[:subsample_size]
        subsample_max = array_sample[-subsample_size:]
        subsample_min_width = np.max(subsample_min) - np.min(subsample_min)
        estimate_min = np.min(subsample_min) - (subsample_min_width**2 / series_sample.size)
        subsample_max_width = np.max(subsample_max) - np.min(subsample_max)
        estimate_max = np.max(subsample_max) + (subsample_max_width**2 / series_sample.size)
        return estimate_min, estimate_max
