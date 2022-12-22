from typing import List

import numpy
from sail_safe_functions_orchestrator.data_frame_federated import DataFrameFederated
from sail_safe_functions_orchestrator.statistics.quantiles import Quantiles
from sail_safe_functions_orchestrator.tools_common import check_instance
from sail_safe_functions_orchestrator.transform.linear import Linear
from sail_safe_functions_orchestrator.transform.scaling import Scaling


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
        for name_feature in list_name_feature_source:
            estimator = Quantiles(quantile_list)
            list_quantile = estimator.run(data_frame[name_feature], quantile_list)
            list_add.append(-min(list_quantile))
            list_multiply.append(1 / (max(list_quantile) - min(list_quantile)))

        array_input = numpy.zeros((len(list_name_feature_source) + 1, len(list_name_feature_source) + 1))
        for i, multiply in enumerate(list_multiply):
            array_input[i, i] = multiply

        transform = Linear()
        result = transform.run(data_frame, array_input, list_name_feature_source, list_name_feature_target, inverse)
        return result
