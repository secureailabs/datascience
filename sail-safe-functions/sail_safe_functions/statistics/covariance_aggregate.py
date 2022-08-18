from typing import Dict, List

from sail_safe_functions.common.tool_moment import sum_dict_moment


class CovarianceAggregate(object):
    """
    Computing the covariance aggregate

    :param object:
    :type object:
    """

    def __init__(self) -> None:
        super().__init__()

    def run(list_dict_moment: List[Dict]) -> float:
        """
        This function run to calculate the final precompute
        and calculate the federated covariance value.

        :param list_list_precompute:
        :type list_list_precompute: List[List[float]]
        :return: covariance
        :rtype: float
        """
        dict_moment = sum_dict_moment(list_dict_moment)

        size_0 = dict_moment["0_0"]
        sum_0 = dict_moment["0_1"]
        size_1 = dict_moment["1_0"]
        sum_1 = dict_moment["1_1"]
        sum_0_1 = dict_moment["0_1_1_1"]

        mean_0 = sum_0 / size_0
        mean_1 = sum_1 / size_1

        term_0 = sum_0_1
        term_1 = -1 * sum_0 * mean_1
        term_2 = -1 * sum_1 * mean_0
        term_3 = size_0 * mean_0 * mean_1

        covariance = (term_0 + term_1 + term_2 + term_3) / (size_0 - 1)
        return covariance
