import pandas


class Concatenate:
    """Wrapper safe function for the pandas concatenate"""

    def run(series_0: pandas.Series, series_1: pandas.Series) -> pandas.Series:
        return pandas.concat([series_0, series_1])
