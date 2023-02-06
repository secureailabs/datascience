from typing import List

import numpy
from sail_safe_functions.aggregator.series_federated import SeriesFederated
from sail_safe_functions.aggregator.statistics.estimator_one_sample import EstimatorOneSample
from sail_safe_functions.participant.statistics.variance_precompute import VariancePrecompute


def variance(
    sample_0: SeriesFederated,
) -> float:
    estimator = Variance()
    return estimator.run(sample_0)


class Variance(EstimatorOneSample):
    """
    Class have run method to perform the federated variance.
    """

    def __init__(
        self,
    ) -> None:
        super().__init__("Variance", ["variance"])

    def run(
        self,
        sample_0: SeriesFederated,
    ) -> float:
        """
        It takes one federated series, and returns the variance of the series

        :param sample_0: sample_0
        :type sample_0: SeriesFederated
        :return: varriance
        :rtype: float
        """
        list_precompute = sample_0.map_function(VariancePrecompute)
        variance = self.aggregate(list_precompute)
        return variance

    def aggregate(
        self,
        list_list_precompute: List[List[float]],
    ) -> float:
        sum_x_0 = 0
        sum_xx_0 = 0
        size_sample_0 = 0

        for list_precompute in list_list_precompute:
            sum_x_0 += list_precompute[0]
            sum_xx_0 += list_precompute[1]
            size_sample_0 += list_precompute[2]

        sample_mean_0 = sum_x_0 / size_sample_0

        sample_variance_0 = ((sum_xx_0 / size_sample_0) - (sample_mean_0 * sample_mean_0)) * (
            size_sample_0 / (size_sample_0 - 1)  # unbiased estimator (numpy version is biased by default)
        )

        return sample_variance_0
