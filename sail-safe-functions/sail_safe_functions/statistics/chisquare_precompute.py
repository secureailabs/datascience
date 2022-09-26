from typing import Dict

import pandas


class ChisquarePrecompute:
    """
    Precomputes data for Chisquare test
    """

    def run(sample_0: pandas.Series, sample_1: pandas.Series) -> Dict:
        """
        Collect the precompute for chisquare

            :param sample_0: First input sample
            :type sample_0: pandas.Series
            :param sample_1: Second input sample
            :type sample_1: pandas.Series
            :return: dicitoanry containing precompute
            :rtype: Dict
        """
        precompute = {}
        for tuple_value in zip(sample_0, sample_1):
            if tuple_value not in precompute:
                precompute[tuple_value] = 0
            precompute[tuple_value] = precompute[tuple_value] + 1

        return precompute
