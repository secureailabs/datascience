import numpy
import pandas
from sail_safe_functions.statistics.variance_agregate import VarianceAggregate
from sail_safe_functions.statistics.variance_precompute import VariancePrecompute
from sail_safe_functions_orchestrator.series_federated import SeriesFederated
from sail_safe_functions_orchestrator.statistics.estimator import Estimator


def variance(sample_0: SeriesFederated):
    estimator = Variance()
    return estimator.Run(sample_0)


class Variance(Estimator):
    def __init__(self) -> None:
        super().__init__(["variance"])

    def Run(self, sample_0: SeriesFederated):
        list_list_precompute = []
        for series in sample_0.dict_series.values():
            list_list_precompute.append(VariancePrecompute.Run(series))
        variance = VarianceAggregate.Run(list_list_precompute)
        return variance

    def run_reference(self, sample_0: SeriesFederated):
        return numpy.var(sample_0.to_numpy(), ddof=1)
