from typing import Dict

import pandas


class ChisquarePrecompute:
    """
    Precomputes data for Chisquare test
    """

    def Run(sample_0: pandas.Series, sample_1: pandas.Series) -> Dict:
        precompute = {}
        for tuple_value in zip(sample_0, sample_1):
            if tuple_value not in precompute:
                precompute[tuple_value] = 0
            precompute[tuple_value] = precompute[tuple_value] + 1

        return precompute
