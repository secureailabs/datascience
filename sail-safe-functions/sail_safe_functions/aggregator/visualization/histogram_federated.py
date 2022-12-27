from collections import Counter
from typing import List

import plotly.express as px
from sail_safe_functions.aggregator.series_federated import SeriesFederated
from sail_safe_functions.aggregator.tools_common import sanitize_dict_for_json
from sail_safe_functions.participant.visualization.histogram_precompute import HistogramPrecompute


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
        >>> from sail_safe_functions.aggregator.visualization.histogram_federated import HistogramFederate
        >>> values = HistogramFederate.Run(sample_0,5)

        Example-2
        --------
        Look into thte notebook

        https://github.com/secureailabs/ScratchPad/blob/master/Saurabh/demo_histogram.ipynb

        It will show you the result in the plot.

        """
        list_precompute = []
        sample_0.map_function(HistogramPrecompute)

        hist_value = HistogramFederate.aggregate(list_precompute)

        fig = px.histogram(hist_value, nbins=bin_count)
        fig_dict = fig.to_dict()
        fig_dict = sanitize_dict_for_json(fig_dict)
        return fig_dict

    # list of precompute contains list of list
    # example list_list_precompute = [ [L1,L2], [L3,L4], [L5, L6] ]
    # L1 -> Unique value for the 1st series.
    # L2 -> Frequency of unique value for the 1st series.
    # L3 -> Unique value for the 2nd series.
    # L4 -> Frequency of unique value for the 2nd series.
    # And so on and on

    @staticmethod
    def aggregate(list_list_precompute: List[List[List[float]]]):
        """
        Function get the aggregated list value counts

        :param list_list_precompute: list
        :type list_list_precompute: List[List[float]]
        :return: values for histogram
        :rtype: value
        """
        print(list_list_precompute)
        final = {}
        for list_precompute in list_list_precompute:
            # initialising dictionaries
            final = Counter(final)
            L1 = list_precompute[0]
            L2 = list_precompute[1]
            ini_dictionary2 = {L1[i]: L2[i] for i in range(len(L1))}
            ini_dictionary2 = Counter(ini_dictionary2)
            # combining dictionaries
            # using Counter
            final = final + ini_dictionary2

        final_list = []
        for key in final:
            for i in range(final[key]):
                final_list.append(key)

        return final_list
