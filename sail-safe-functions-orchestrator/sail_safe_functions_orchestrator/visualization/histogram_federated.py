import plotly.express as px
from sail_safe_functions.visualization.histogram_aggregate import HistogramAggregate
from sail_safe_functions.visualization.histogram_precompute import HistogramPrecompute
from sail_safe_functions_orchestrator.series_federated import SeriesFederated


class HistogramFederate:
    @staticmethod
    def hist(sample_0: SeriesFederated, bin_count: int):
        """
        Main histogram function

        :param sample_0: _description_
        :type sample_0: SeriesFederated
        :param bin_count: _description_
        :type bin_count: int
        :return: _description_
        :rtype: _type_
        """

        list_list_precompute = []
        for series in sample_0.dict_series.values():
            list_list_precompute.append(HistogramPrecompute.run(series))

        hist_value = HistogramAggregate.run(list_list_precompute)
        fig = px.histogram(hist_value, nbins=bin_count)
        return fig

    @staticmethod
    def run(sample_0: SeriesFederated, bin_count: int):
        """
        Runs federated histogram function

        :param sample_0: _description_
        :type sample_0: SeriesFederated
        :param bin_count: _description_
        :type bin_count: int
        :return: _description_
        :rtype: _type_
        """
        return HistogramFederate.hist(sample_0, bin_count)
