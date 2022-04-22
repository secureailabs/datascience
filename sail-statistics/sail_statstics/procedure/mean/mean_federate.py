from sail_statstics.orchestrator.series_federated import SeriesFederated

from sail_statstics.procedure.mean.mean_precompute import MeanPrecompute
from sail_statstics.procedure.mean.mean_agregate import MeanAgregate


class MeanFederate:
    @staticmethod
    def mean(sample_0: SeriesFederated):

        list_list_precompute = []
        list_dict_series = list(sample_0.dict_series.keys())
        for key in list_dict_series:
            list_list_precompute.append(MeanPrecompute.run(sample_0.dict_series[key]))

        mean_statistic = MeanAgregate.run(list_list_precompute)

        return mean_statistic
