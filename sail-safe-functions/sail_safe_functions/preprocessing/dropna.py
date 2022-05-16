from typing import Any

import pandas as pd


class DropNa:
    """
    Drop rows or columns with missing data
    """

    def Run(data_frame: pd.DataFrame, axis: int, how: str, thresh: int, subset: Any) -> pd.DataFrame:
        """
        Remove missing values.
        See the :ref:`User Guide <missing_data>` for more on which values are
        considered missing, and how to work with missing data.
        Parameters
        ----------
        axis : {0 or 'index', 1 or 'columns'}, default 0
            Determine if rows or columns which contain missing values are
            removed.
            * 0, or 'index' : Drop rows which contain missing values.
            * 1, or 'columns' : Drop columns which contain missing value.
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
        return data_frame.dropna(axis=axis, how=how, thresh=thresh, subset=subset, inplace=False)
