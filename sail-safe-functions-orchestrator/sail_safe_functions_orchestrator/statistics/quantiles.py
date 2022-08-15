from typing import List

import numpy
from sail_safe_functions_orchestrator import preprocessing
from sail_safe_functions_orchestrator.series_federated import SeriesFederated
from sail_safe_functions_orchestrator.statistics.estimator import Estimator
from scipy import interpolate


def quantiles(sample_0: SeriesFederated, list_quantile) -> List[float]:
    estimator = Quantiles(list_quantile)
    return estimator.run(sample_0)


class Quantiles(Estimator):
    """
    Class that wraps the safe function for min and max
    """

    def __init__(self, list_quantile: List[float]) -> None:
        list_name_quantile = [str(quantile) for quantile in list_quantile]
        super().__init__(list_name_quantile)
        self.list_quantile = list_quantile

    def run(self, sample_0: SeriesFederated) -> List[float]:
        array_domain, array_value = preprocessing.cdf(sample_0)
        return interpolate.interp1d(array_value, array_domain)(self.list_quantile)

    def run_reference(self, sample_0: SeriesFederated, list_quantile) -> List[float]:
        return numpy.quantile(sample_0.to_numpy(), list_quantile)
