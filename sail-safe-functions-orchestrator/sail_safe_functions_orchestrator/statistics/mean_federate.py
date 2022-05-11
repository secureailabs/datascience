import numpy
import pandas
from sail_safe_functions.statistics.mean_agregate import MeanAgregate
from sail_safe_functions.statistics.mean_precompute import MeanPrecompute
from sail_safe_functions_orchestrator.series_federated import SeriesFederated


class MeanFederate:
    @staticmethod
    def mean(sample_0: SeriesFederated):

        list_list_precompute = []
        for series in sample_0.dict_series.values():
            list_list_precompute.append(MeanPrecompute.run(series))

        mean_statistic = MeanAgregate.run(list_list_precompute)

        return mean_statistic

    @staticmethod
    def Run(sample_0: SeriesFederated):
        return MeanFederate.mean(sample_0)

    @staticmethod
    def RunReference(sample_0: pandas.Series):
        return numpy.mean(sample_0.to_numpy())
