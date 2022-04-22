from sail_safe_functions_orchestrator.series_federated import SeriesFederated
from sail_safe_functions.statistics.mean_precompute import MeanPrecompute
from sail_safe_functions.statistics.mean_agregate import MeanAgregate


class MeanFederate:
    @staticmethod
    def mean(sample_0: SeriesFederated):

        list_list_precompute = []
        for series in sample_0.dict_series.values():
            list_list_precompute.append(MeanPrecompute.run(series))

        mean_statistic = MeanAgregate.run(list_list_precompute)

        return mean_statistic
