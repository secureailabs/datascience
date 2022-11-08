from typing import Any, List, Union

from sail_safe_functions.preprocessing.impute_univariate_precompute import ImputeUnivariatePrecompute
from sail_safe_functions_orchestrator.data_frame_federated import DataFrameFederated
from sail_safe_functions_orchestrator.tools_common import check_instance


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
        data_frame_source: DataFrameFederated,
        list_series_name: List[str],
        missing_value: Union[str, int, float],
    ) -> DataFrameFederated:
        check_instance(data_frame_source, DataFrameFederated)
        list_reference = []
        for dataset_id in data_frame_source.list_dataset_id:
            client = data_frame_source.service_client.get_client(dataset_id)
            reference_data_frame = data_frame_source.dict_reference_data_frame[dataset_id]
            list_reference.append(
                client.call(ImputeUnivariatePrecompute, reference_data_frame, list_series_name, missing_value)
            )
        return DataFrameFederated(
            data_frame_source.service_client, list_reference, data_frame_source.data_model_data_frame
        )
