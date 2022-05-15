from typing import Tuple

from sail_safe_functions_orchestrator.preprocessing.rank_federate import RankFederate
from sail_safe_functions_orchestrator.series_federated import SeriesFederated
from sail_safe_functions_orchestrator.statistics.pearson_federate import PearsonFederate
from scipy import stats
from scipy.stats import t


class SpearmanFederate:

    """
    SpearmanFederate
    """

    @staticmethod
    def spearman(
        sample_0: SeriesFederated, sample_1: SeriesFederated, alternative: str, mode: str
    ) -> Tuple[float, float]:
        """spearman
        Computes the spearman coeffcient by ranking both sample and

        :param sample_0: sample 0
        :type sample_0: SeriesFederated
        :param sample_1: sample 1
        :type sample_1: SeriesFederated
        :param alternative: The alternative to be tested: `two-sided`, `less` or `greater`
        :type alternative: str
        :param mode: The mode for which to run the ranking algoritm in must be `unsafe` or `cdf` where `unsafe`
        is unsafe and must be refactored out before this ends up in production
        :type mode: str
        :raises ValueError: raise a ValueError if `alternative` is not `two-sided`, `less` or `greater`
        :raises ValueError: raise a ValueError if `mode` is not  `unsafe` or `cdf`
        :raises ValueError: raise a ValueError if samples are not of equal size
        :return: returns
        :rtype: Tuple[float, float]
        """

        if alternative not in {"two-sided", "less", "greater"}:
            raise ValueError("alternative must be `two-sided`, `less` or `greater`")
        if mode not in {"unsafe", "cdf"}:
            raise ValueError("mode must be `unsafe` or `cdf`")

        if sample_0.size != sample_1.size:
            raise ValueError("samples must be of equal size")

        rank_0 = RankFederate.run(sample_0, mode)
        rank_1 = RankFederate.run(sample_1, mode)
        return PearsonFederate.pearson(rank_0, rank_1, alternative)

    @staticmethod
    def run(sample_0: SeriesFederated, sample_1: SeriesFederated, alternative: str, mode: str) -> Tuple[float, float]:
        return SpearmanFederate.spearman(sample_0, sample_1, alternative, mode)

    @staticmethod
    def run_reference(sample_0: SeriesFederated, sample_1: SeriesFederated, alternative: str) -> Tuple[float, float]:
        return stats.spearmanr(sample_0.to_numpy(), sample_1.to_numpy(), alternative=alternative)
