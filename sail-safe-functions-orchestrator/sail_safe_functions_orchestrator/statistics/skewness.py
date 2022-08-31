from typing import Tuple

from sail_safe_functions.statistics.skewness_aggregate import SkewnessAggregate
from sail_safe_functions.statistics.skewness_precompute import SkewnessPrecompute
from sail_safe_functions_orchestrator.series_federated import SeriesFederated
from sail_safe_functions_orchestrator.statistics.estimator import Estimator
from scipy import stats


def skewness(
    sample_0: SeriesFederated,
) -> Tuple[float]:

    estimator = Skewness()
    return estimator.run(sample_0)


class Skewness(Estimator):

    """
    An estimator for Skewness
    """

    def __init__(self) -> None:
        super().__init__(["skewness"])

    def run(self, sample_0: SeriesFederated):
        """
        It takes one federated series, and returns the skewness value of the series.

        :param sample_0: sample series
        :type sample_0: SeriesFederated
        :return: skewness value of series
        :rtype: float
        """
        list_list_precompute = []

        # TODO deal with posibilty sample_0 and sample_1 do net share same child frames

        # Calculating precompute
        for series in sample_0.dict_series.values():
            list_list_precompute.append(SkewnessPrecompute.run(series))

        # Final Skew Value
        skewness = SkewnessAggregate.run(list_list_precompute)
        return skewness

    def run_reference(self, sample_0: SeriesFederated):
        return stats.skew(sample_0.to_numpy())
