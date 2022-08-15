import pandas


class LinearPrecompute:
    """
    Do a linear transform
    """

    def run(sample_0: pandas.Series, add: float, multiply: float):
        sample_0_tranformed = (sample_0 + add) * multiply
        return sample_0_tranformed
