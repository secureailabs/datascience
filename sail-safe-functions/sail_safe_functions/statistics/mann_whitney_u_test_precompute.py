import pandas


class MannWhitneyUTestPrecompute:
    """
    The precompute function of the mann withnet u test
    """

    def run(
        series_0: pandas.Series, series_concatenated_ranked: pandas.Series
    ) -> float:
        """
        precompute function of the mann withnet u test
        
        :param series_0: _description_
        :type series_0: pandas.Series
        :param series_concatenated_ranked: _description_
        :type series_concatenated_ranked: pandas.Series
        :return: _description_
        :rtype: float
        """
        return series_concatenated_ranked[: series_0.size].sum()
