import pandas


class MannWhitneyUTestPrecompute:
    """
    The precompute function of the mann withnet u test
    """

    def run(
        series_0: pandas.Series, series_concatenated_ranked: pandas.Series
    ) -> float:
        return series_concatenated_ranked[: series_0.size].sum()
