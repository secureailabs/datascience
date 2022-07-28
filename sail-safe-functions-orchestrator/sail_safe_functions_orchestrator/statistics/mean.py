import numpy
import pandas
from sail_safe_functions.statistics.mean_agregate import MeanAggregate
from sail_safe_functions.statistics.mean_precompute import MeanPrecompute
from sail_safe_functions_orchestrator.series_federated import SeriesFederated
from sail_safe_functions_orchestrator.statistics.estimator import Estimator


def mean(sample_0: SeriesFederated):
    estimator = Mean()
    return estimator.Run(sample_0)


class Mean(Estimator):
    def __init__(self) -> None:
        super().__init__(["mean"])

    def Run(self, sample_0: SeriesFederated):
        list_list_precompute = []
        for series in sample_0.dict_series.values():
            list_list_precompute.append(MeanPrecompute.Run(series))
        mean_statistic = MeanAggregate.Run(list_list_precompute)
        return mean_statistic

    def run_reference(self, sample_0: SeriesFederated):
        return numpy.mean(sample_0.to_numpy())
