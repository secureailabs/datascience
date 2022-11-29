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

        # TODO deal with posibilty sample_0 and sample_1 do net share same child frames

        # Calculating precompute
        list_list_precompute = []
        for dataset_id in sample_0.list_dataset_id:
            client = sample_0.service_client.get_client(dataset_id)
            reference_series_0 = sample_0.get_reference_series(dataset_id)
            list_list_precompute.append(client.call(KurtosisPrecompute, reference_series_0))

        # Final Kurtosis Value
        kurtosis_value = KurtosisAggregate.run(list_list_precompute)
        return kurtosis_value

    def run_reference(self, sample_0: SeriesFederated):
        return stats.kurtosis(sample_0.to_numpy())
