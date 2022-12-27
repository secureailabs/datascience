from collections import Counter
from typing import List

import plotly.figure_factory as ff
from sail_safe_functions.aggregator.series_federated import SeriesFederated
from sail_safe_functions.aggregator.tools_common import sanitize_dict_for_json
from sail_safe_functions.participant.visualization.kernel_density_estimation_precompute import (
    KernelDensityEstimationPrecompute,
)


def kernel_density_estimation(sample_0: SeriesFederated, bin_size: float):
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

    return KernelDensityEstimation.run(sample_0, bin_size)


class KernelDensityEstimation:
    """
    Performs the federated kernel density estimation.

    """

    @staticmethod
    def run(sample_0: SeriesFederated, bin_size: float):
        list_precompute = sample_0.map_function(KernelDensityEstimationPrecompute)
        kde_value = KernelDensityEstimation.aggregate(list_precompute)
        list_kde_value = [kde_value]
        list_group_label = [sample_0.series_name]
        fig = ff.create_distplot(list_kde_value, list_group_label, bin_size)
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
    def aggregate(list_list_precompute: List[List[float]]):
        """
        Function get the aggregated list value counts

        :param list_list_precompute: list
        :type list_list_precompute: List[List[float]]
        :return: values for histogram
        :rtype: value
        """
        final = {}
        for precompute in list_list_precompute:
            # initialising dictionaries
            final = Counter(final)
            L1 = precompute[0]
            L2 = precompute[1]
            dict_values = {L1[i]: L2[i] for i in range(len(L1))}
            dict_values = Counter(dict_values)
            # combining dictionaries
            # using Counter
            final = final + dict_values

        final_list = []
        for key in final:
            for i in range(final[key]):
                final_list.append(key)

        return final_list
