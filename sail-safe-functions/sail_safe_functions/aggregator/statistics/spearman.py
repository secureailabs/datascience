from itertools import count
from typing import Tuple

from sail_safe_functions.aggregator import preprocessing, statistics
from sail_safe_functions.aggregator.series_federated import SeriesFederated
from sail_safe_functions.aggregator.statistics.estimator_two_sample import EstimatorTwoSample
from sail_safe_functions.aggregator.tools_common import check_series_constant
from scipy import stats


def spearman(
    sample_0: SeriesFederated,
    sample_1: SeriesFederated,
    alternative: str,
    type_ranking: str,
) -> Tuple[float, float]:
    """
    It takes two federated series, and returns the rho and the p-value

    :param sample_0: sample 0
    :type sample_0: SeriesFederated
    :param sample_1: sample 1
    :type sample_1: SeriesFederated
    :param alternative: The alternative to be tested: `two-sided`, `less` or `greater`
    :type alternative: str
    :param type_ranking: The mode for which to run the ranking algoritm in must be `unsafe` or `cdf` where `unsafe`
    is unsafe and must be refactored out before this ends up in production
    :type type_ranking: str
    :raises ValueError: raise a ValueError if `alternative` is not `two-sided`, `less` or `greater`
    :raises ValueError: raise a ValueError if `type_ranking` is not  `unsafe` or `cdf`
    :raises ValueError: raise a ValueError if samples are not of equal size
    :return: returns
    :rtype: Tuple[float, float]
    """

    estimator = Spearman(alternative, type_ranking)
    return estimator.run(sample_0, sample_1)


class Spearman(EstimatorTwoSample):

    """
    The Spearman correlation estimator
    """

    def __init__(self, alternative: str, type_ranking: str) -> None:
        super().__init__(f"Spearman - {alternative} - {type_ranking}", ["rho", "p_value"])
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
        count_0 = statistics.count(sample_0)
        count_1 = statistics.count(sample_1)
        if count_0 != count_1:
            raise ValueError("samples must be of equal size")
        # TODO Here we should check the series is constant but it should be work on the federated ranking
        # it should be included in a different ticket.
        # https://secureailabs.atlassian.net/browse/BOARD-2068
        # check_series_constant(sample_0)
        # check_series_constant(sample_1)
        rank_0 = preprocessing.rank(sample_0, self.type_ranking)
        rank_1 = preprocessing.rank(sample_1, self.type_ranking)
        rho, p_value = statistics.pearson(rank_0, rank_1, self.alternative)
        return rho, p_value

    def run_reference(
        self,
        sample_0: SeriesFederated,
        sample_1: SeriesFederated,
    ) -> Tuple[float, float]:
        return stats.spearmanr(sample_0.to_numpy(), sample_1.to_numpy(), alternative=self.alternative)
