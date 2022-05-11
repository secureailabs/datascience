from typing import Tuple

import pandas
from sail_safe_functions.statistics.skewness_agregate import SkewnessAgregate
from sail_safe_functions.statistics.skewness_precompute import SkewnessPrecompute
from sail_safe_functions_orchestrator.series_federated import SeriesFederated
from scipy import stats


class SkewnessFederate:

    """
    Final function to run for skewness Fedrated
    :return: Tupel[Float]
    :rtype: _type_
    """

    @staticmethod
    def skewness(
        sample_0: SeriesFederated,
    ) -> Tuple[float]:

        list_list_precompute = []

        # TODO deal with posibilty sample_0 and sample_1 do net share same child frames

        # Calculating precompute
        for series in sample_0.dict_series.values():
            list_list_precompute.append(SkewnessPrecompute.run(series))

        # Final Skew Value
        skew_value = SkewnessAgregate.run(list_list_precompute)
        return skew_value

    @staticmethod
    def Run(sample_0: SeriesFederated):
        return SkewnessFederate.skewness(sample_0)

    @staticmethod
    def RunReference(sample_0: pandas.Series):
        return stats.skew(sample_0.to_numpy())
