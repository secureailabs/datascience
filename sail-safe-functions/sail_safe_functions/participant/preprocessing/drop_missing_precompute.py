from typing import Any

from sail_safe_functions.aggregator.data_frame import DataFrame
from sail_safe_functions.aggregator.reference_data_frame import ReferenceDataFrame
from sail_safe_functions.aggregator.series import Series
from sail_safe_functions.aggregator.service_reference import ServiceReference
from sail_safe_functions.safe_function_base import SafeFunctionBase


class DropMissingPrecompute(SafeFunctionBase):
    """
    Drop rows or columns with missing data
    """

    def run(
        reference_data_frame_source: ReferenceDataFrame, axis: int, how: str, thresh: int, subset: Any
    ) -> ReferenceDataFrame:
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
            DataFrame without the rows dropped NA entries dropped.
        """
        data_frame_source = ServiceReference.get_instance().reference_to_data_frame(reference_data_frame_source)
        data_frame_target_pandas = data_frame_source.dropna(
            axis=axis, how=how, thresh=thresh, subset=subset, inplace=False
        )
        list_series = []
        for series_name in data_frame_target_pandas.columns:
            series_pandas = data_frame_target_pandas[series_name]
            series = Series.from_pandas(
                data_frame_source.dataset_id, data_frame_source.data_model_data_frame[series_name], series_pandas
            )
            series.index = series_pandas.index
            list_series.append(series)
        data_frame_target = DataFrame(data_frame_source.dataset_id, data_frame_source.data_frame_name, list_series)
        reference_data_frame_target = ServiceReference.get_instance().data_frame_to_reference(data_frame_target)
        return reference_data_frame_target
