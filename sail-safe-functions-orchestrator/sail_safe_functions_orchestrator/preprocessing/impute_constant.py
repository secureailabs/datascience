from typing import List, Union

from sail_safe_functions.preprocessing.impute_constant_precompute import (
    ImputeConstantPrecompute,
)
from sail_safe_functions_orchestrator.data_frame_federated import DataFrameFederated
from sail_safe_functions_orchestrator.tools_common import check_instance


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

    def run(
        data_frame_source: DataFrameFederated,
        list_name_column: List[str],
        missing_value: Union[str, int, float],
    ) -> DataFrameFederated:
        check_instance(data_frame_source, DataFrameFederated)
        data_frame_target = data_frame_source.create_new()
        for dataset_id in data_frame_source.dict_dataframe:
            data_frame_target.dict_dataframe[dataset_id] = ImputeConstantPrecompute.run(
                data_frame_source.dict_dataframe[dataset_id],
                list_name_column,
                missing_value,
            )
        return data_frame_target
