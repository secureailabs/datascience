from typing import List, Tuple

import numpy
import scipy
from sail_core.implementation_manager import ImplementationManager
from sail_safe_functions.aggregator import preprocessing, statistics
from sail_safe_functions.aggregator.series_federated import SeriesFederated
from sail_safe_functions.aggregator.statistics.estimator_two_sample import EstimatorTwoSample
from sail_safe_functions.aggregator.tools_common import (
    check_series_empty_federated,
    check_series_one_value_federated,
    check_series_paired,
)
from sail_safe_functions.participant.statistics.wilcoxon_signed_rank_test_precompute import (
    WilcoxonSingedRankTestPrecompute,
)


def wilcoxon_singed_rank_test(
    sample_0: SeriesFederated,
    sample_1: SeriesFederated,
    alternative: str,
    type_ranking: str,
) -> Tuple[float, float]:
    estimator = WilcoxonSingedRankTest(alternative, type_ranking)
    return estimator.run(sample_0, sample_1)


class WilcoxonSingedRankTest(EstimatorTwoSample):
    """
    This class contains method for federated Wilcoxon Singed Rank Test
    """

    def __init__(
        self,
        alternative: str,
        type_ranking: str,
    ) -> None:
        super().__init__(f"WilcoxonSingedRankTest - {alternative} - {type_ranking}", ["w_statistic", "p_value"])
        if alternative not in ["less", "two-sided", "greater"]:
            raise ValueError('Alternative must be of "less", "two-sided" or "greater"')
        if type_ranking not in {"unsafe", "cdf"}:
            raise ValueError("`type_ranking` must be `unsafe` or `cdf`")
        self.alternative = alternative
        self.type_ranking = type_ranking

    def run(
        self,
        sample_0: SeriesFederated,
        sample_1: SeriesFederated,
    ) -> Tuple[float, float]:
        """
        It takes two federated series, and returns the p-value and w_statistic of the Wilcoxon Singed Rank Test

        :param sample_0: first sample series
        :type sample_0: SeriesFederated
        :param sample_1: Second sample series
        :type sample_1: SeriesFederated
        :raises ValueError: raise error for value error
        :raises Exception: raise error for exception
        :return: w_statistic, p_value
        :rtype: float, float
        """

        check_series_paired(sample_0, sample_1)
        check_series_empty_federated(sample_0)
        check_series_empty_federated(sample_1)
        check_series_one_value_federated(
            sample_0
        )  # No need to check the other because the series are checked to be paired

        size_sample = statistics.count(sample_0)
        (
            sample_difference,
            sample_difference_absolute,
        ) = preprocessing.wilcoxon_singed_rank_test_difference_tranform(sample_0, sample_1)
        sample_difference_absolute_ranked = preprocessing.rank(sample_difference_absolute, self.type_ranking)

        # Calculating precompute
        list_precompute = []
        participant_service = ImplementationManager.get_instance().get_participant_service()
        for dataset_id in sample_difference.list_dataset_id:
            reference_series_difference = sample_difference.dict_reference_series[dataset_id]
            reference_series_difference_absolute_ranked = sample_difference_absolute_ranked.dict_reference_series[
                dataset_id
            ]
            list_precompute.append(
                participant_service.call(
                    dataset_id,
                    WilcoxonSingedRankTestPrecompute,
                    reference_series_difference,
                    reference_series_difference_absolute_ranked,
                )
            )

        # rank_minus rank_plus
        rank_minus, rank_plus = self.aggregate(list_precompute)

        if self.alternative == "two-sided":
            w_statistic = min(rank_minus, rank_plus)
        else:
            w_statistic = rank_plus

        mean = size_sample * (size_sample + 1.0) * 0.25
        standard_deviation = numpy.sqrt(size_sample * (size_sample + 1.0) * (2.0 * size_sample + 1.0) / 24)
        z_statistic = (w_statistic - mean) / standard_deviation

        if self.alternative == "two-sided":
            p_value = 2.0 * scipy.stats.distributions.norm.sf(abs(z_statistic))
        elif self.alternative == "less":
            p_value = scipy.stats.distributions.norm.cdf(z_statistic)
        elif self.alternative == "greater":
            p_value = scipy.stats.distributions.norm.sf(z_statistic)
        else:
            raise Exception()

        return w_statistic, p_value

    def aggregate(
        self,
        list_precompute: List,
    ) -> Tuple[float, float]:
        rank_minus = 0
        rank_plus = 0
        for precompute in list_precompute:
            rank_minus += precompute[0]
            rank_plus += precompute[1]
        return rank_minus, rank_plus
