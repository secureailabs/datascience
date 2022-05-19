from typing import List

import pandas


class WeightedSum:
    """
    Takes the weighted sum of a list of series
    """

    def run(list_series: List[pandas.Series], list_weight: List[float]) -> pandas.Series:
        """Takes the weighted sum of a list of series

        :param list_series:list of series to be weighted
        :type list_series: List[pandas.Series]
        :param list_weight list of weights
        :type list_weight: List[float]
        :raises ValueError: raises a value exception if `list_series` and `list_weight` are not of equal lenght
        :return: returns a new series that is a weighted sum
        :rtype: pandas.Series
        """
        if len(list_series) != len(list_weight):
            raise ValueError("`list_series` and `list_weight` must be of same lenght")
        series_sum = list_series[0] * 0
        for series, weight in zip(list_series, list_weight):
            series_sum += series * weight
        return series_sum
