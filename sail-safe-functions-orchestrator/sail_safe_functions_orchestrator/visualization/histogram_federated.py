import plotly.express as px
from sail_safe_functions.visualization.histogram_aggregate import HistogramAggregate
from sail_safe_functions.visualization.histogram_precompute import HistogramPrecompute
from sail_safe_functions_orchestrator.series_federated import SeriesFederated


def histogram_federated(sample_0: SeriesFederated, bin_count: int):
    return HistogramFederate.run(sample_0, bin_count)


class HistogramFederate:
    @staticmethod
    def run(sample_0: SeriesFederated, bin_count: int):
        """
        Performs the federated histogram.
        It take on federated series and bin count. Returns the histogram.
        -----------
            :param sample_0: The first sample of data
            :type sample_0: SeriesFederated
            :param bin_count: The second sample of data
            :type bin_count: int
            :return: pyplot figure valuie
            :rtype: pyplot object

        it works to segregate the range into several bins and then returns the number
        of instances in each bin. This function is used to build the histogram.

        A histogram is an approximate representation of the distribution of numerical data.
        The term was first introduced by Karl Pearson.[1] To construct a histogram, the first step
        is to "bin" (or "bucket") the range of values—that is, divide the entire range of values
        into a series of intervals—and then count how many values fall into each interval.
        The bins are usually specified as consecutive, non-overlapping intervals of a variable.
        The bins (intervals) must be adjacent and are often (but not required to be) of equal size.[2]

        If the bins are of equal size, a rectangle is erected over the bin with height proportional to
        the frequency—the number of cases in each bin. A histogram may also be normalized to display
        "relative" frequencies. It then shows the proportion of cases that fall into each of several
        categories, with the sum of the heights equaling 1.
        -----------

        Example
        -----------
        >>> from sail_safe_functions_orchestrator.visualization.histogram_federated import HistogramFederate
        >>> values = HistogramFederate.Run(sample_0,5)

        Example-2
        --------
        Look into thte notebook

        https://github.com/secureailabs/ScratchPad/blob/master/Saurabh/demo_histogram.ipynb

        It will show you the result in the plot.

        """
        list_list_precompute = []
        for dataset_id in sample_0.list_dataset_id:
            client = sample_0.service_client.get_client(dataset_id)
            list_list_precompute.append(
                client.call(
                    HistogramPrecompute,
                    sample_0.dict_reference_series[dataset_id],
                )
            )
        hist_value = HistogramAggregate.run(list_list_precompute)

        fig = px.histogram(hist_value, nbins=bin_count)
        fig_dict = fig.to_dict()
        fig_dict["data"][0]["x"] = list(fig_dict["data"][0]["x"])
        return fig_dict
