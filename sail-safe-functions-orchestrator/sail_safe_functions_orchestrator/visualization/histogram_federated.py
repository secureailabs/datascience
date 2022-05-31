import numpy
import pandas
from sail_safe_functions.visualization.histogram_agregate import HistogramAgregate
from sail_safe_functions.visualization.histogram_precompute import HistogramPrecompute
from sail_safe_functions_orchestrator.series_federated import SeriesFederated


class HistogramFederate:
    @staticmethod
    def hist(sample_0: SeriesFederated):

        list_list_precompute = []
        for series in sample_0.dict_series.values():
            list_list_precompute.append(HistogramPrecompute.run(series))

        hist_value = HistogramAgregate.run(list_list_precompute)

        return hist_value

    @staticmethod
    def Run(sample_0: SeriesFederated):
        return HistogramFederate.hist(sample_0)
