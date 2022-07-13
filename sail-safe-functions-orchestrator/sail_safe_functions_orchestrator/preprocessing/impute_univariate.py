from typing import Any, List, Union

from sail_safe_functions.preprocessing.impute_univariate_precompute import ImputeUnivariatePrecompute
from sail_safe_functions_orchestrator.data_frame_federated import DataFrameFederated
from sail_safe_functions_orchestrator.tools_common import ToolsCommon


def impute_univariate(
    data_frame_source: DataFrameFederated, list_name_column: List[str], strategy: str
) -> DataFrameFederated:
    """Imputes one or more columns with a univariate strategy

    :param data_frame: Input dataframe
    :type data_frame: DataFrameFederated
    :param list_name_column: a list of column names to impute, set to None to do all columns
    :type list_name_column: list[str]
    :param strategy: strategy, must be either `mean`, `median` or `most_frequent`, on non-numerical data only must frequent is valid
    :type strategy: str
    :return: Output dataframe
    :rtype: DataFrameFederated
    """

    return ImputeUnivariate.run(data_frame_source, list_name_column, strategy)


class ImputeUnivariate:
    """
    class for ImputeUnivariate
    """

    def run(
        data_frame_source: DataFrameFederated, list_name_column: List[str], missing_value: Union[str, int, float]
    ) -> DataFrameFederated:
        ToolsCommon.check_instance(data_frame_source, DataFrameFederated)
        data_frame_target = data_frame_source.create_new()
        for dataset_id in data_frame_source.dict_dataframe:
            data_frame_target.dict_dataframe[dataset_id] = ImputeUnivariatePrecompute.run(
                data_frame_source.dict_dataframe[dataset_id], list_name_column, missing_value
            )
        return data_frame_target
