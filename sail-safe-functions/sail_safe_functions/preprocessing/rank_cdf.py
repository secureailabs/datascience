from typing import List

import numpy
from pandas import Series
from scipy import interpolate


class RankCdf:
    """
    Agregates data for a federated cdf
    """

    def run(
        sample_0: Series,
        size_sample_total: int,
        list_domain_cdf: List[float],
        list_value_cdf: List[float],
    ) -> Series:
        array_sample_0 = sample_0
        function_cdf = interpolate.interp1d(numpy.array(list_domain_cdf), numpy.array(list_value_cdf))
        array_rank = numpy.round(function_cdf(array_sample_0) * size_sample_total)
        return Series(array_rank, name=f"{sample_0.name}_ranked")
