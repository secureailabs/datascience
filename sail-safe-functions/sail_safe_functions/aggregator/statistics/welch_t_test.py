import math
from typing import List, Tuple

import numpy as np
from sail_core.implementation_manager import ImplementationManager
from sail_safe_functions.aggregator.series_federated import SeriesFederated
from sail_safe_functions.aggregator.statistics.estimator_two_sample import EstimatorTwoSample
from sail_safe_functions.aggregator.tools_common import check_series_one_value_federated, check_variance_zero
from sail_safe_functions.participant.statistics.unpaired_t_test_precompute import UnpairedTTestPrecompute
from scipy.stats import t


def welch_t_test(
    sample_0: SeriesFederated,
    sample_1: SeriesFederated,
    alternative: str = "less",
) -> Tuple[float, float]:
    estimator = WelchTTest(alternative)
    return estimator.run(sample_0, sample_1)


class WelchTTest(EstimatorTwoSample):
    """
    This class contains method for federated Welch T test
    """

    def __init__(
        self,
        alternative,
    ) -> None:
        super().__init__(f"WelchTTest - {alternative}", ["t_statistic", "p_value"])
        if alternative not in ["less", "two-sided", "greater"]:
            raise ValueError('Alternative must be of "less", "two-sided" or "greater"')
        self.alternative = alternative

    def run(
        self,
        sample_0: SeriesFederated,
        sample_1: SeriesFederated,
    ) -> Tuple[float, float]:
        """
        Perform federated Welch T test.
        It takes two federated series, and returns the p-value and test statistic of the Levene test

        :param sample_0: First series sample
        :type sample_0: SeriesFederated
        :param sample_1: Second series sample
        :type sample_1: SeriesFederated
        :return: t_statistic, p_value
        :rtype: Float, Float
        """
        check_series_one_value_federated(sample_0)
        check_series_one_value_federated(sample_1)

        list_list_precompute = []
        # TODO deal with posibilty sample_0 and sample_1 do net share same child frames
        participant_service = ImplementationManager.get_instance().get_participant_service()
        for dataset_id in sample_0.list_dataset_id:
            reference_series_0 = sample_0.get_reference_series(dataset_id)
            reference_series_1 = sample_1.get_reference_series(dataset_id)
            list_list_precompute.append(
                participant_service.call(
                    dataset_id,
                    UnpairedTTestPrecompute,
                    reference_series_0,
                    reference_series_1,
                )
            )

        t_statistic, degrees_of_freedom = self.aggregate(list_list_precompute)
        p_value = t.cdf(t_statistic, degrees_of_freedom)
        if self.alternative == "less":
            p_value = t.cdf(t_statistic, degrees_of_freedom)
        elif self.alternative == "two-sided":
            p_value = t.cdf(t_statistic, degrees_of_freedom) / 2
        elif self.alternative == "greater":
            p_value = 1 - t.cdf(t_statistic, degrees_of_freedom)
        else:
            raise ValueError()
        return t_statistic, p_value

    def aggregate(
        self,
        list_list_precompute: List[List[float]],
    ) -> Tuple[float, float]:
        sum_x_0 = 0
        sum_xx_0 = 0
        size_sample_0 = 0
        sum_x_1 = 0
        sum_xx_1 = 0
        size_sample_1 = 0
        for list_precompute in list_list_precompute:
            sum_x_0 += list_precompute[0]
            sum_xx_0 += list_precompute[1]
            size_sample_0 += list_precompute[2]
            sum_x_1 += list_precompute[3]
            sum_xx_1 += list_precompute[4]
            size_sample_1 += list_precompute[5]

        sample_mean_0 = sum_x_0 / size_sample_0
        sample_variance_0 = ((sum_xx_0 / size_sample_0) - (sample_mean_0 * sample_mean_0)) * (
            size_sample_0 / (size_sample_0 - 1)  # unbiased estimator (numpy version is biased by default)
        )
        check_variance_zero(sample_variance_0)

        sample_mean_1 = sum_x_1 / size_sample_1
        sample_variance_1 = ((sum_xx_1 / size_sample_1) - (sample_mean_1 * sample_mean_1)) * (
            size_sample_1 / (size_sample_1 - 1)  # unbiased estimator (np version is biased by default)
        )
        check_variance_zero(sample_variance_1)
        t_statistic = (sample_mean_0 - sample_mean_1) / (
            np.sqrt((sample_variance_0 / size_sample_0) + (sample_variance_1 / size_sample_1))
        )
        # Welch–Satterthwaite equation:
        degrees_of_freedom_numerator = math.pow(
            ((sample_variance_0 / size_sample_0) + (sample_variance_1 / size_sample_1)),
            2,
        )
        degrees_of_freedom_denominator = (
            math.pow(sample_variance_0, 2) / (size_sample_0 * size_sample_0 * (size_sample_0 - 1))
        ) + (math.pow(sample_variance_1, 2) / (size_sample_1 * size_sample_1 * (size_sample_1 - 1)))
        degrees_of_freedom = degrees_of_freedom_numerator / degrees_of_freedom_denominator

        return t_statistic, degrees_of_freedom
