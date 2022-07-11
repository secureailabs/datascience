import numpy
import pandas
from sail_safe_functions.statistics.mean_agregate import MeanAgregate
from sail_safe_functions.statistics.mean_precompute import MeanPrecompute
from sail_safe_functions_orchestrator.series_federated import SeriesFederated
from sail_safe_functions_orchestrator.statistics.estimator import Estimator


class MeanFederate(Estimator):
    def __init__(self) -> None:
        super().__init__()
        self.list_name_estimate = ["mean"]

    @staticmethod
    def mean(sample_0: SeriesFederated):
        estimator = MeanFederate()
        return estimator.run(sample_0)

    def run(self, sample_0: SeriesFederated):
        list_list_precompute = []
        for series in sample_0.dict_series.values():
            list_list_precompute.append(MeanPrecompute.run(series))
        mean_statistic = MeanAgregate.run(list_list_precompute)
        return mean_statistic

    def run_reference(self, sample_0: SeriesFederated):
        return numpy.mean(sample_0.to_numpy())
