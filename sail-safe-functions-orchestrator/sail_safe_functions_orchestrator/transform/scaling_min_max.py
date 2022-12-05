from typing import List

import numpy
from sail_safe_functions_orchestrator import transform
from sail_safe_functions_orchestrator.data_frame_federated import \
    DataFrameFederated
from sail_safe_functions_orchestrator.transform.scaling_quantile import \
    ScalingQuantile


class ScalingMinMax:
    """
    Scaling min max transforms

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
        transform = ScalingQuantile()
        result = transform.run(data_frame, list_name_feature_source, list_name_feature_target, quantile_list, inverse)

        return result
