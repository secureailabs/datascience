from typing import List

import pandas as pd


class ColumnSelect:
    """
    Select a column with a specific name
    """

    def Run(data_frame: pd.DataFrame, name_column: str) -> pd.Series:
        return data_frame[name_column]
