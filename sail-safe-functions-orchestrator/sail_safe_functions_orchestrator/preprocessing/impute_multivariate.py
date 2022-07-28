from typing import Any, List, Union

from sail_safe_functions.preprocessing.impute_multivariate_precompute import (
    ImputeMultivariatePrecompute,
)
from sail_safe_functions_orchestrator.data_frame_federated import DataFrameFederated
from sail_safe_functions_orchestrator.tools_common import check_instance


def impute_multivariate(
    data_frame_source: DataFrameFederated,
    list_name_column: List[str],
    imputation_order: str,
    max_iter: int = 10,
) -> DataFrameFederated:
    """Imputes one or more columns with a multivariate strategy

    :param data_frame: Input dataframe
    :type data_frame: DataFrameFederated
    :param list_name_column: a list of column names to impute, set to None to do all columns
    :type list_name_column: list[str]
    :param imputation_order: imputation_order, must be {`ascending`, `descending`}
        `ascending` From features with fewest missing values to most.
        `descending`: From features with most missing values to fewest.
    :type imputation_order: str
    :param max_iter: (default=10) maximum number of imputation rounds to perform before returning the imputations computed during the final round.
        The stopping criterion is met once max(abs(X_t - X_{t-1}))/max(abs(X[known_vals])) < tol, where X_t is X at iteration t.
    :type max_iter: int
    :return: Output dataframe
    :rtype: DataFrameFederated
    """
    return ImputeMultivariate.Run(
        data_frame_source, list_name_column, imputation_order, max_iter
    )


class ImputeMultivariate:
    """
    class for ImputeMultivariate
    """

    def Run(
        data_frame_source: DataFrameFederated,
        list_name_column: List[str],
        imputation_order: str,
        max_iter: int = 10,
    ) -> DataFrameFederated:
        check_instance(data_frame_source, DataFrameFederated)
        data_frame_target = data_frame_source.create_new()
        for dataset_id in data_frame_source.dict_dataframe:
            data_frame_target.dict_dataframe[
                dataset_id
            ] = ImputeMultivariatePrecompute.Run(
                data_frame_source.dict_dataframe[dataset_id],
                list_name_column,
                imputation_order,
                max_iter,
            )
        return data_frame_target
