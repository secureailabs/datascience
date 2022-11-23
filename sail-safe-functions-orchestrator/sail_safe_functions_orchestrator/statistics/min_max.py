from typing import Tuple

import numpy
from sail_safe_functions.statistics.min_max_aggregate import MinMaxAggregate
from sail_safe_functions.statistics.min_max_precompute import MinMaxPrecompute
from sail_safe_functions_orchestrator.series_federated import SeriesFederated
from sail_safe_functions_orchestrator.statistics.estimator import Estimator


def min_max(sample_0: SeriesFederated) -> Tuple[float, float]:
    estimator = MinMax()
    return estimator.run(sample_0)


class MinMax(Estimator):
    """
    Class that wraps the safe function for min and max
    """

    def __init__(self) -> None:
        super().__init__(["min", "max"])

    def run(self, sample_0: SeriesFederated) -> Tuple[float, float]:
        """
        Perform federated min max.
        It takes one federated series, and returns min and max value for it.

        :param sample_0: sample series
        :type sample_0: SeriesFederated
        :return: min and max value
        :rtype: Tuple[float, float]
        """
        list_list_precompute = []
        # TODO deal with posibilty sample_0 and sample_1 do not share same child frames

        # Calculating precompute
        for dataset_id in sample_0.list_dataset_id:
            client = sample_0.service_client.get_client(dataset_id)
            reference_series_0 = sample_0.get_reference_series(dataset_id)
            list_list_precompute.append(client.call(MinMaxPrecompute, reference_series_0))

        # Final min max values
        min, max = MinMaxAggregate.run(list_list_precompute)
        return min, max

    def run_reference(self, sample_0: SeriesFederated) -> Tuple[float, float]:
        min_numpy = numpy.min(sample_0.to_numpy())  # TODO this is ugly as fuck
        max_numpy = numpy.max(sample_0.to_numpy())
        return min_numpy, max_numpy
