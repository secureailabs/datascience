import numpy
import pandas
from sail_safe_functions.statistics.variance_agregate import VarianceAgregate
from sail_safe_functions.statistics.variance_precompute import VariancePrecompute
from sail_safe_functions_orchestrator.series_federated import SeriesFederated


class VarianceFederate:
    @staticmethod
    def variance(sample_0: SeriesFederated):

        list_list_precompute = []
        for series in sample_0.dict_series.values():
            list_list_precompute.append(VariancePrecompute.run(series))

        mean_statistic = VarianceAgregate.run(list_list_precompute)

        return mean_statistic

    @staticmethod
    def run(sample_0: SeriesFederated):
        return VarianceFederate.variance(sample_0)

    @staticmethod
    def run_reference(sample_0: SeriesFederated):
        return numpy.var(sample_0.to_numpy(), ddof=1)
