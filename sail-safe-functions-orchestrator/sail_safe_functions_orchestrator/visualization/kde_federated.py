import plotly.figure_factory as ff
from sail_safe_functions.visualization.kde_aggregate import KdeAggregate
from sail_safe_functions.visualization.kde_precompute import KdePrecompute
from sail_safe_functions_orchestrator.series_federated import SeriesFederated


class KdeFederate:
    @staticmethod
    def kde(sample_0: SeriesFederated):
        """
        Performs the federated kernel density estimation.
        It take on federated series and bin count. Returns the kde plot.
        -----------
            :param sample_0: The first sample of data
            :type sample_0: SeriesFederated
            :param bin_count: The second sample of data
            :type bin_count: int
            :return: pyplot figure valuie
            :rtype: pyplot object

        """
        list_list_precompute = []
        for series in sample_0.dict_series.values():
            list_list_precompute.append(KdePrecompute.run(series))

        kde_value = KdeAggregate.run(list_list_precompute)
        fig = ff.create_distplot(kde_value)
        return fig

    @staticmethod
    def run(sample_0: SeriesFederated):
        return KdeFederate.kde(sample_0)
