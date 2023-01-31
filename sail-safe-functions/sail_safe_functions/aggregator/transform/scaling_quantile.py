from typing import List

import numpy
from sail_safe_functions.aggregator.data_frame_federated import DataFrameFederated
from sail_safe_functions.aggregator.statistics.quantiles import Quantiles
from sail_safe_functions.aggregator.transform.linear import Linear


class ScalingQuantile:
    """ScalingQuantile transforms a dataframe with only numbers
    to a dataframe where all values are scaled between a lower and a upper quantile

    """

    @staticmethod
    def run(
        data_frame: DataFrameFederated,
        list_name_feature_source: List[str],
        list_name_feature_target: List[str],
        quantile_list,
        inverse: bool,
    ):
        """
        Federated Scaling function based on Quantile list

        :param data_frame: Federated Dataframe
        :type data_frame: DataFrameFederated
        :param list_name_feature_source: List of series for transform
        :type list_name_feature_source: List[str]
        :param list_name_feature_target: neww list of series name
        :type list_name_feature_target: List[str]
        :param quantile_list: qunatile values
        :type quantile_list: List
        :return: added scaled feature to federated DataFrame
        :rtype: federated DataFrame
        """

        list_add = []
        list_multiply = []
        array_size = len(list_name_feature_source) + 1

        for name_feature in list_name_feature_source:
            estimator = Quantiles()
            list_quantile = estimator.run(data_frame[name_feature], quantile_list)
            scale = max(list_quantile) - min(list_quantile)
            list_add.append(-min(list_quantile) / scale)
            list_multiply.append(1 / scale)

        array_input = numpy.zeros((array_size, array_size))
        for i in range(array_size - 1):
            array_input[i, i] = list_multiply[i]
            array_input[array_size - 1, i] = list_add[i]
        array_input[array_size - 1, array_size - 1] = 1

        transform = Linear()
        result = transform.run(data_frame, array_input, list_name_feature_source, list_name_feature_target, inverse)
        return result
