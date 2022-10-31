import plotly.figure_factory as ff
from sail_safe_functions.visualization.kde_aggregate import KdeAggregate
from sail_safe_functions.visualization.kde_precompute import KdePrecompute
from sail_safe_functions_orchestrator.series_federated import SeriesFederated


class Kde:
    @staticmethod
    def kde(sample_0: SeriesFederated, group_labels: str, bin_size: float):
        """
        Performs the federated kernel density estimation.
        It take on federated series and bin count. Returns the kde plot.
        -----------
            :param sample_0: The first sample of data
            :type sample_0: SeriesFederated
            :param bin_size: The second sample of data
            :type bin_size: float
            :return: pyplot figure valuie
            :rtype: pyplot object

        """
        list_list_precompute = []
        for series in sample_0.dict_series.values():
            list_list_precompute.append(KdePrecompute.run(series))

        kde_value = KdeAggregate.run(list_list_precompute)
        fig = ff.create_distplot(kde_value, group_labels, bin_size)
        return fig

    @staticmethod
    def run(sample_0: SeriesFederated, group_labels: str, bin_size: float):
        return Kde.kde(sample_0, group_labels, bin_size)
