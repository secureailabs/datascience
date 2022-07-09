import plotly.express as px
from sail_safe_functions.visualization.histogram_agregate import HistogramAgregate
from sail_safe_functions.visualization.histogram_precompute import HistogramPrecompute
from sail_safe_functions_orchestrator.series_federated import SeriesFederated


class HistogramFederate:
    @staticmethod
    def hist(sample_0: SeriesFederated, bin_count: int):

        list_list_precompute = []
        for series in sample_0.dict_series.values():
            list_list_precompute.append(HistogramPrecompute.run(series))

        hist_value = HistogramAgregate.run(list_list_precompute)
        fig = px.histogram(hist_value, nbins=bin_count)
        return fig

    @staticmethod
    def Run(sample_0: SeriesFederated, bin_count: int):
        return HistogramFederate.hist(sample_0, bin_count)
