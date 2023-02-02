from typing import List

import numpy
from sail_safe_functions.aggregator.series_federated import SeriesFederated
from sail_safe_functions.aggregator.statistics.estimator_one_sample import EstimatorOneSample
from sail_safe_functions.participant.statistics.mean_precompute import MeanPrecompute


def mean(sample_0: SeriesFederated):
    """
    Perform federated Mean.
    It takes one federated series, and returns the mean value

    :param sample_0: sample series
    :type sample_0: SeriesFederated
    :return: mean value of federated series
    :rtype: float
    """
    estimator = Mean()
    return estimator.run(sample_0)


class Mean(EstimatorOneSample):
    def __init__(self) -> None:
        super().__init__("Mean", ["mean"])

    def run(self, sample_0: SeriesFederated):
        """
        It takes one federated series, and returns the mean

        :param sample_0: _description_
        :type sample_0: SeriesFederated
        :return: mean
        :rtype: float
        """

        list_precompute = sample_0.map_function(MeanPrecompute)

        mean_statistic = self.aggregate(list_precompute)
        return mean_statistic

    def aggregate(self, list_list_precompute: List[List[float]]) -> float:
        sum_x_0 = 0
        degrees_of_freedom_0 = 0

        for list_precompute in list_list_precompute:
            sum_x_0 += list_precompute[0]
            degrees_of_freedom_0 += list_precompute[1]

        sample_mean_0 = sum_x_0 / degrees_of_freedom_0

        # if degrees_of_freedom < 20:
        #     raise Exception()
        return sample_mean_0

    def run_reference(self, sample_0: SeriesFederated):
        return numpy.mean(sample_0.to_numpy())
