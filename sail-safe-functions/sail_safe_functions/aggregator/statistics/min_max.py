from typing import List, Tuple

import numpy
from sail_safe_functions.aggregator.series_federated import SeriesFederated
from sail_safe_functions.aggregator.statistics.estimator_one_sample import EstimatorOneSample
from sail_safe_functions.aggregator.tools_common import check_series_empty_federated
from sail_safe_functions.participant.statistics.min_max_precompute import MinMaxPrecompute


def min_max(
    sample_0: SeriesFederated,
) -> Tuple[float, float]:
    estimator = MinMax()
    return estimator.run(sample_0)


class MinMax(EstimatorOneSample):
    """
    Class that wraps the safe function for min and max
    """

    def __init__(
        self,
    ) -> None:
        super().__init__("MinMax", ["min", "max"])

    def run(
        self,
        sample_0: SeriesFederated,
    ) -> Tuple[float, float]:
        """
        Perform federated min max.
        It takes one federated series, and returns min and max value for it.

        :param sample_0: sample series
        :type sample_0: SeriesFederated
        :return: min and max value
        :rtype: Tuple[float, float]
        """

        check_series_empty_federated(sample_0)
        list_precompute = []
        # TODO deal with posibilty sample_0 and sample_1 do not share same child frames

        # Calculating precompute
        list_precompute = sample_0.map_function(MinMaxPrecompute)

        # Final min max values
        min, max = self.aggregate(list_precompute)
        return min, max

    def aggregate(
        self,
        list_tuple_min_max: List[Tuple[float, float]],
    ) -> Tuple[float, float]:
        """Aggregates the results of multiple precompute functions into a global min and max

        :param list_tuple_min_max: A list of tuples from various precompute functions
        :type list_tuple_min_max: List[Tuple[float, float]]
        :return: return the federated estimated sample min max
        :rtype: Tuple[float, float]
        """
        list_min = []
        list_max = []
        for tuple_min_max in list_tuple_min_max:
            list_min.append(tuple_min_max[0])
            list_max.append(tuple_min_max[1])
        return min(list_min), max(list_max)
