from typing import List

import pandas as pd


class HistogramPrecompute:
    """
    Precomputes data for Kurtosis
    """

    def run(sample_0_series: pd.Series) -> List[float]:
        """Generates the precompute count Frequency for use in a histogram

        Parameters
        ----------
        sample_0_series : pd.series
            The series for sample_0
        Returns
        -------
        return two list :
        list_1 : Unique values in the series
        list_2 : list of frequecy(count of total number of time each vallue came in the seires) of every unique value.
        """
        # series containing unique value in index and frequency.
        series = sample_0_series.value_counts()
        l1 = list(series.index)
        l2 = list(series)

        list_precompute = [l1, l2]

        return list_precompute
