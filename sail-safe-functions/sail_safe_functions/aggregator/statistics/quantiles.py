from typing import List

import numpy
from sail_safe_functions.aggregator import preprocessing
from sail_safe_functions.aggregator.series_federated import SeriesFederated
from sail_safe_functions.aggregator.statistics.estimator import Estimator
from scipy import interpolate


def quantiles(sample_0: SeriesFederated, list_quantile) -> List[float]:
    estimator = Quantiles(list_quantile)
    return estimator.run(sample_0, list_quantile)


class Quantiles(Estimator):
    """
    Class that wraps the safe function for min and max
    """

    @staticmethod
    def run(sample_0: SeriesFederated, list_quantile):
        """
        Method to find quantiles for the series

        :param sample_0: Sample series
        :type sample_0: SeriesFederated
        :param list_quantile: Quantile list you want
        :type list_quantile: List
        :return: List of qunatile value for each list_quamtile
        :rtype: List
        """
        array_domain, array_value = preprocessing.cumulative_distribution_function(sample_0)
        return interpolate.interp1d(array_value, array_domain)(list_quantile)

    def run_reference(self, sample_0: SeriesFederated, list_quantile):
        return numpy.quantile(sample_0.to_numpy(), list_quantile)
