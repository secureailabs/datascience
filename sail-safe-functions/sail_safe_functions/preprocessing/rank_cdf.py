from typing import List

import numpy
from pandas import Series
from scipy import interpolate


class RankCumulativeDistributionFunction:
    """
    Aggregates data for a federated cdf
    """

    def run(
        sample_0: Series,
        size_sample_total: int,
        list_domain_cdf: List[float],
        list_value_cdf: List[float],
    ) -> Series:
        """
        Rank the cdf

            :param sample_0: input sample
            :type sample_0: Series
            :param size_sample_total: value for sample size
            :type size_sample_total: int
            :param list_domain_cdf: A 1-D array of real value
            :type list_domain_cdf: List[float]
            :param list_value_cdf: A N-D array of real values. The length of y along the interpolation axis must be equal to the length of x
            :type list_value_cdf: List[float]
            :return: array containing rank
            :rtype: Series
        """
        array_sample_0 = sample_0
        function_cdf = interpolate.interp1d(numpy.array(list_domain_cdf), numpy.array(list_value_cdf))
        array_rank = numpy.round(function_cdf(array_sample_0) * size_sample_total)
        return Series(array_rank, name=f"{sample_0.name}_ranked")
