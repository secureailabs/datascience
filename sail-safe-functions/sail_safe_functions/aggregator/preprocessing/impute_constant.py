from typing import Any, List, Union

from sail_core.tools_common import check_instance
from sail_safe_functions.aggregator.data_frame_federated import DataFrameFederated
from sail_safe_functions.participant.preprocessing.impute_constant_precompute import ImputeConstantPrecompute


def impute_constant(
    data_frame_source: DataFrameFederated,
    list_name_column: List[str],
    missing_value: Union[str, int, float],
) -> DataFrameFederated:
    """Imputes one or more columns with a constant value

    :param data_frame: Input data_frame
    :type data_frame: DataFrameFederated
    :param list_name_column: a list of column names to impute, set to None to do all columns
    :type list_name_column: list[str]
    :param missing_value: a string int or float value with wich to impute
    :type missing_value: Union[str, int, float]
    :raises ValueError: raises a ValueError if missing_value is neither numeric or string
    :raises ValueError: raises a ValueError if missing_value type does not match selected columns
    :return: Output data_frame
    :rtype: DataFrameFederated
    """
    return ImputeConstant.run(data_frame_source, list_name_column, missing_value)


class ImputeConstant:
    """
    class for ImputeConstant
    """

    @staticmethod
    def run(
        data_frame_source: DataFrameFederated,
        list_series_name: List[str],
        missing_value: Union[str, int, float],
    ) -> DataFrameFederated:
        check_instance(data_frame_source, DataFrameFederated)
        list_reference = data_frame_source.map_function(ImputeConstantPrecompute, list_series_name, missing_value)

        return DataFrameFederated(list_reference, data_frame_source.data_model_data_frame)
