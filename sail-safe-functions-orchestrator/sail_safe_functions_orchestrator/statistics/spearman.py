from typing import Tuple

from sail_safe_functions_orchestrator import statistics
from sail_safe_functions_orchestrator.preprocessing.rank_federate import RankFederate
from sail_safe_functions_orchestrator.series_federated import SeriesFederated
from sail_safe_functions_orchestrator.statistics.estimator import Estimator
from sail_safe_functions_orchestrator.statistics.pearson import Pearson
from scipy import stats


def spearman(
    sample_0: SeriesFederated, sample_1: SeriesFederated, alternative: str, type_ranking: str
) -> Tuple[float, float]:
    """spearman
    Computes the spearman coeffcient by ranking both sample and

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


class Spearman(Estimator):

    """
    The Spearman correlation estimator
    """

    def __init__(self, alternative, type_ranking: str) -> None:
        super().__init__(["rho", "p_value"])
        if alternative not in ["less", "two-sided", "greater"]:
            raise ValueError('Alternative must be of "less", "two-sided" or "greater"')
        if type_ranking not in {"unsafe", "cdf"}:
            raise ValueError("`type_ranking` must be `unsafe` or `cdf`")
        self.alternative = alternative
        self.type_ranking = type_ranking

    def run(self, sample_0: SeriesFederated, sample_1: SeriesFederated) -> Tuple[float, float]:
        if sample_0.size != sample_1.size:
            raise ValueError("samples must be of equal size")

        rank_0 = RankFederate.run(sample_0, self.type_ranking)
        rank_1 = RankFederate.run(sample_1, self.type_ranking)
        rho, p_value = statistics.pearson(rank_0, rank_1, self.alternative)
        return rho, p_value

    def run_reference(self, sample_0: SeriesFederated, sample_1: SeriesFederated) -> Tuple[float, float]:
        return stats.spearmanr(sample_0.to_numpy(), sample_1.to_numpy(), alternative=self.alternative)
