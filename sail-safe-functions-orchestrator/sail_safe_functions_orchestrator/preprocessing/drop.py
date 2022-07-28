from typing import Any

from sail_safe_functions.preprocessing.drop_precompute import DropPrecompute
from sail_safe_functions_orchestrator.data_frame_federated import DataFrameFederated
from sail_safe_functions_orchestrator.tools_common import check_instance


def drop(
    data_frame_source: DataFrameFederated,
    labels: list,
    axis: int,
    index: list,
    columns: list,
    level: int,
    errors: str,
) -> DataFrameFederated:
    """
    Drop specified labels from rows or columns.
    Remove rows or columns by specifying label names and corresponding axis, or by
    specifying directly index or column names. When using a multi-index, labels on different
    levels can be removed by specifying the level.

    :param data_frame: dataframe to operate on
    :type data_frame: pd.DataFrame
    :param labels: single label or list-like
        Index or column labels to drop. A tuple will be used as a single label and not treated as a list-like.
    :type labels: list
    :param axis: {0 or `index`, 1 or `columns`}, default 0
        Whether to drop labels from the index (0 or `index`) or columns (1 or `columns`).
    :type axis: int
    :param index: single label or list-like
        Alternative to specifying axis (labels, axis=0 is equivalent to index=labels).
    :type index: list
    :param columns: single label or list-like
        Alternative to specifying axis (labels, axis=1 is equivalent to columns=labels).
    :type columns: list
    :param level: int or level name, optional
        For MultiIndex, level from which the labels will be removed.
    :type level: int
    :param errors: {`ignore`, `raise`}, default `raise`
        If `ignore`, suppress error and only existing labels are dropped.
    :type errors: str
    :return: DataFrame with specified entries dropped.
    :rtype: pd.DataFrame
    """
    return Drop.run(
        data_frame_source,
        labels,
        axis,
        index,
        columns,
        level,
        errors,
    )


class Drop:
    """
    Drop rows or columns with missing data
    """

    def run(
        data_frame_source: DataFrameFederated,
        labels: list,
        axis: int,
        index: list,
        columns: list,
        level: int,
        errors: str,
    ) -> DataFrameFederated:
        check_instance(data_frame_source, DataFrameFederated)
        data_frame_target = data_frame_source.create_new()
        for dataset_id in data_frame_source.dict_dataframe:
            data_frame_target.dict_dataframe[dataset_id] = DropPrecompute.Run(
                data_frame_source.dict_dataframe[dataset_id],
                labels,
                axis,
                index,
                columns,
                level,
                errors,
            )
        return data_frame_target
