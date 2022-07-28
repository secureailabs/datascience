from typing import List

import pandas


# TODO this function is dangerous
class ValueAbsolute:
    """
    Takes the absolute value sum of a series
    """

    def Run(series_0: pandas.Series) -> pandas.Series:
        """Takes the weighted sum of a list of series

        :param series_0: input series
        :type series_0: pandas.Series
        :return: returns a new series that is a absolute value
        :rtype: pandas.Series
        """

        return series_0.abs()
