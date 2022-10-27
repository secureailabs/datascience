from typing import Any

from sail_safe_functions.preprocessing.drop_missing_precompute import DropMissingPrecompute
from sail_safe_functions_orchestrator.data_frame_federated import DataFrameFederated
from sail_safe_functions_orchestrator.tools_common import check_instance


def drop_series_with_missing(
    data_frame_source: DataFrameFederated, how: str, thresh: int, subset: Any
) -> DataFrameFederated:
    """
    Remove missing values.
    Parameters
    ----------
    how : {'any', 'all'}, default 'any'
        Determine if row or column is removed from DataFrame, when we have
        at least one NA or all NA.
        * 'any' : If any NA values are present, drop that row or column.
        * 'all' : If all values are NA, drop that row or column.
    thresh : int, optional
        Require that many non-NA values. Cannot be combined with how.
    subset : column label or sequence of labels, optional
        Labels along other axis to consider, e.g. if you are dropping rows
        these would be a list of columns to include.

    Returns
    -------
    DataFrame
        DataFrame with NA entries dropped.
    """
    return DropSeriesWithMissing.run(data_frame_source, how, thresh, subset)


class DropSeriesWithMissing:
    """
    Drop rows or columns with missing data
    """

    def run(
        data_frame_source: DataFrameFederated,
        how: str,
        thresh: int,
        subset: Any,
    ) -> DataFrameFederated:
        check_instance(data_frame_source, DataFrameFederated)
        data_frame_target = data_frame_source.create_new()
        for dataset_id in data_frame_source.dict_dataframe:
            data_frame_target.dict_dataframe[dataset_id] = DropMissingPrecompute.run(
                data_frame_source.dict_dataframe[dataset_id], 1, how, thresh, subset
            )
        return data_frame_target
