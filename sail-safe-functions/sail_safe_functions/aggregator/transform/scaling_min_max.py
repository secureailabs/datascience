from typing import List

from sail_safe_functions.aggregator.data_frame_federated import DataFrameFederated
from sail_safe_functions.aggregator.transform.scaling_quantile import ScalingQuantile


def scaling_min_max(
    data_frame: DataFrameFederated,
    list_name_feature_source: List[str],
    list_name_feature_target: List[str],
    inverse: bool,
):
    """
    :param data_frame: Federated Dataframe
    :type data_frame: DataFrameFederated
    :param list_name_feature_source: List of series for transform
    :type list_name_feature_source: List[str]
    :param list_name_feature_target: neww list of series name
    :type list_name_feature_target: List[str]
    :param inverse: To do inverse linear transform
    :type inverse: bool
    :return: added scaled feature to federated DataFrame
    :rtype: federated DataFrame
    """
    ScalingMinMax.run(data_frame, list_name_feature_source, list_name_feature_target, inverse)


class ScalingMinMax:
    """
    Scaling min max transforms

    """

    @staticmethod
    def run(
        data_frame: DataFrameFederated,
        list_name_feature_source: List[str],
        list_name_feature_target: List[str],
        inverse: bool,
    ):

        transform = ScalingQuantile()
        result = transform.run(data_frame, list_name_feature_source, list_name_feature_target, [0, 1], inverse)

        return result
