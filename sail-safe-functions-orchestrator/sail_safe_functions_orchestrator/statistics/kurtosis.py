from typing import Tuple
from sail_safe_functions.statistics.kurtosis_aggregate import KurtosisAggregate
from sail_safe_functions.statistics.kurtosis_precompute import KurtosisPrecompute
from sail_safe_functions_orchestrator.series_federated import SeriesFederated
from sail_safe_functions_orchestrator.statistics.estimator import Estimator
from scipy import stats


def kurtosis(sample_0: SeriesFederated) -> Tuple[float]:
    """
    Perform federated kurtosis.
    It takes one federated series, and returns the kurtosis value of the series

    :param sample_0: sample series
    :type sample_0: SeriesFederated
    :return: Kurtosis value
    :rtype: Tuple[float]
    """
    estimator = Kurtosis()
    return estimator.run(sample_0)


class Kurtosis(Estimator):
    """
    A estimator for Kurtosis
    """

    def __init__(self) -> None:
        super().__init__(["kurtosis"])

    def run(self, sample_0: SeriesFederated):
        list_list_precompute = []
        # TODO deal with posibilty sample_0 and sample_1 do net share same child frames

        # Calculating precompute
        for series in sample_0.dict_series.values():
            list_list_precompute.append(KurtosisPrecompute.run(series))

        # Final Kurtosis Value
        kurtosis_value = KurtosisAggregate.run(list_list_precompute)
        return kurtosis_value

    def run_reference(self, sample_0: SeriesFederated):
        return stats.kurtosis(sample_0.to_numpy())
