from typing import List

import pandas


class SelectColumnPrecompute:
    """
    Selects specific columns
    """

    def run(
        data_frame: pandas.DataFrame,
        list_name_column: List[str],
    ) -> pandas.DataFrame:
        return data_frame[list_name_column]
