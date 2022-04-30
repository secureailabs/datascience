from typing import Union

import numpy as np
import pandas as pd
from pandas.api.types import is_numeric_dtype, is_string_dtype


class ImputeConstant:
    """
    Imputes one or more columns with a constant value
    """

    def Run(
        data_frame: pd.DataFrame, list_name_column: list[str], missing_value: Union[str, int, float]
    ) -> pd.DataFrame:
        """Imputes one or more columns with a constant value

        :param data_frame: Input data_frame
        :type data_frame: pd.DataFrame
        :param list_name_column: a list of column names to impute, set to None to do all columns
        :type list_name_column: list[str]
        :param missing_value: a string int or float value with wich to impute
        :type missing_value: Union[str, int, float]
        :raises ValueError: raises a ValueError if missing_value is neither numeric or string
        :raises ValueError: raises a ValueError if missing_value type does not match selected columns
        :return: Output data_frame
        :rtype: pd.DataFrame
        """
        if type(missing_value) == int or type(missing_value) == float:
            missing_type_numberic = True
        elif type(missing_value) == str:
            missing_type_numberic = False
        else:
            raise ValueError("missing_value is neither numeric nor a string")

        data_frame = data_frame.copy()
        if list_name_column is None:
            list_name_column = list(data_frame.columns)
        for name_column in list_name_column:
            if missing_type_numberic and not is_numeric_dtype(data_frame[name_column]):
                raise ValueError("missing_value is numeric type but column with name " + name_column + " is not")
            if not missing_type_numberic and not is_string_dtype(data_frame[name_column]):
                raise ValueError("missing_value is string type but column with name " + name_column + " is not")
            data_frame[name_column] = data_frame[name_column].replace(np.nan, missing_value)
        return data_frame
