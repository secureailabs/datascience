from typing import List, Union

import numpy as np
import pandas as pd
from pandas.api.types import is_numeric_dtype, is_string_dtype
from sail_safe_functions_orchestrator.data_frame import DataFrame
from sail_safe_functions_orchestrator.reference_data_frame import ReferenceDataFrame
from sail_safe_functions_orchestrator.series import Series
from sail_safe_functions_orchestrator.service_reference import ServiceReference


class ImputeConstantPrecompute:
    """
    Imputes one or more columns with a constant value
    """

    def run(
        reference_data_frame_source: ReferenceDataFrame,
        list_series_name: List[str],
        missing_value: Union[str, int, float],
    ) -> pd.DataFrame:
        """Imputes one or more columns with a constant value

        :param data_frame: Input data_frame
        :type data_frame: pd.DataFrame
        :param list_series_name: a list of seires names to impute, set to None to do all columns
        :type list_series_name: list[str]
        :param missing_value: a string int or float value with wich to impute
        :type missing_value: Union[str, int, float]
        :raises ValueError: raises a ValueError if missing_value is neither numeric or string
        :raises ValueError: raises a ValueError if missing_value type does not match selected columns
        :return: Output data_frame
        :rtype: pd.DataFrame
        """
        if type(missing_value) == int or type(missing_value) == float:
            missing_type_numeric = True
        elif type(missing_value) == str:
            missing_type_numeric = False
        else:
            raise ValueError("missing_value is neither numeric nor a string")

        data_frame_source = ServiceReference.get_instance().reference_to_data_frame(reference_data_frame_source)
        if list_series_name is None:
            list_series_name = data_frame_source.list_series_name
        list_series = []
        for series_name in list_series_name:
            if missing_type_numeric and not is_numeric_dtype(data_frame_source[series_name]):
                raise ValueError(f"missing_value is numeric type but series with series_name {series_name} is not")
            if not missing_type_numeric and not is_string_dtype(data_frame_source[series_name]):
                raise ValueError(f"missing_value is string type but series with series_name {series_name} is not")
            series_pandas = data_frame_source[series_name].replace(np.nan, missing_value)
            list_series.append(
                Series.from_pandas(series_name, data_frame_source[series_name].data_model_series, series_pandas)
            )
        data_frame_target = DataFrame(data_frame_source.dataset_id, data_frame_source.data_frame_name, list_series)
        reference_data_frame_target = ServiceReference.get_instance().data_frame_to_reference(data_frame_target)
        return reference_data_frame_target
