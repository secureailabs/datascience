from typing import List

import numpy
from pandas import Series
from scipy import stats


class KolmogorovSmirnovTestPrecompute:
    """
    Precomputes data for the KolmogorovSmirnov test
    """

    def run(sample_0: Series, sample_ranked_0: Series, distribution: str, count_total: int) -> List[float]:
        """
        Calculate the preceomputes for KolmogorovSmirnov test

            :param sample_0: First input sample
            :type sample_0: Series
            :param sample_ranked_0: Second input sample
            :type sample_ranked_0: Series
            :param distribution: Type of distribution ypu want to have
            :type distribution: str
            :param count_total: total count
            :type count_total: int
            :return: KS Test precompute
            :rtype: List[float]
        """
        type_distribution = distribution["type_distribution"]

        array_sample_0 = sample_0.to_numpy()
        array_sample_ranked_0 = sample_ranked_0.to_numpy()

        if type_distribution == "normal":
            sample_mean = numpy.mean(array_sample_0)
            sample_sdev = numpy.std(array_sample_0, ddof=1)
            array_value_cdf = stats.norm.cdf(array_sample_0, loc=sample_mean, scale=sample_sdev)
        elif type_distribution == "normalunit":
            array_value_cdf = stats.norm.cdf(array_sample_0, loc=0, scale=1)
        else:
            raise Exception()
        return numpy.max(numpy.abs((array_sample_ranked_0 / count_total) - array_value_cdf))
