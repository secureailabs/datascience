from typing import Dict

import pandas


class ChisquarePrecompute:
    """
    Precomputes data for Chisquare test
    """

    def run(sample_0: pandas.Series, sample_1: pandas.Series) -> Dict:
        """
        collect the precompute for chisquare

        :param sample_0: _description_
        :type sample_0: pandas.Series
        :param sample_1: _description_
        :type sample_1: pandas.Series
        :return: _description_
        :rtype: Dict
        """
        precompute = {}
        for tuple_value in zip(sample_0, sample_1):
            if tuple_value not in precompute:
                precompute[tuple_value] = 0
            precompute[tuple_value] = precompute[tuple_value] + 1

        return precompute
