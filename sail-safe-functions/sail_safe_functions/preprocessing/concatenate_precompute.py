import pandas


class ConcatenatePrecompute:
    """Wrapper safe function for the pandas concatenate"""

    def run(series_0: pandas.Series, series_1: pandas.Series) -> pandas.Series:
        """
        Wraaper function to conncatenate two pandas series.

        :param series_0: first input series
        :type series_0: pandas.Series
        :param series_1: Second input series
        :type series_1: pandas.Series
        :return:concatenating all Series along the index (axis=0), a series is returned.
        :rtype: pandas.Series
        """
        return pandas.concat([series_0, series_1])
