import pandas as pd


class DropPrecompute:
    """
    Drop specific rows or columns
    """

    def run(
        data_frame: pd.DataFrame,
        labels: list,
        axis: int,
        index: list,
        columns: list,
        level: int,
        errors: str,
    ) -> pd.DataFrame:
        """Drop specified labels from rows or columns.
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
        return data_frame.drop(
            labels=labels, axis=axis, index=index, columns=columns, level=level, inplace=False, errors=errors
        )
