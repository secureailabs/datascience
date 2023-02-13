from typing import Any, List, Union

from sail_core.tools_common import check_instance
from sail_safe_functions.aggregator.data_frame_federated import DataFrameFederated
from sail_safe_functions.participant.preprocessing.impute_multivariate_precompute import ImputeMultivariatePrecompute


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
    return ImputeMultivariate.run(data_frame_source, list_name_column, imputation_order, max_iter)


class ImputeMultivariate:
    """
    class for ImputeMultivariate
    """

    @staticmethod
    def run(
        data_frame_source: DataFrameFederated,
        list_name_column: List[str],
        imputation_order: str,
        max_iter: int = 10,
    ) -> DataFrameFederated:
        check_instance(data_frame_source, DataFrameFederated)

        list_reference = data_frame_source.map_function(
            ImputeMultivariatePrecompute,
            list_name_column,
            imputation_order,
            max_iter,
        )
        return DataFrameFederated(list_reference, data_frame_source.data_model_data_frame)
