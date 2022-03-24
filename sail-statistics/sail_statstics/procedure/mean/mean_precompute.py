from typing import Any, List, Tuple

import pandas as pd
import numpy as np


class MeanPrecompute(object):
    def __init__(self) -> None:
        super().__init__()

    def run(
        sample_0_dataframe: pd.DataFrame,
    ) -> Tuple[List[float], List[bool]]:  # there seems to be a problem here with this annotation
        sample_0 = sample_0_dataframe.to_numpy()

        sum_x_0 = np.sum(sample_0)
        sample_0_dof = len(sample_0)

        list_precompute = [sum_x_0, sample_0_dof]
        # list_safe = [False, False, False, False, False, False ]
        return list_precompute  # , list_safe
