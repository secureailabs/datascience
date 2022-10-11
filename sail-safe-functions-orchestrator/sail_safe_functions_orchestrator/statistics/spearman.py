from typing import Tuple

from sail_safe_functions_orchestrator.data import utils
from sail_safe_functions_orchestrator.statistics.pearson import pearson
from scipy import stats


def spearman(
    clients,
    sample_0: list,
    sample_1: list,
    alternative: str = "less",
) -> Tuple[float, float]:
    if len(sample_0) != len(sample_1):
        raise ValueError("samples must be of equal size")

    rank_0 = utils.rank_cdf(clients, sample_0)
    rank_1 = utils.rank_cdf(clients, sample_1)
    rho, p_value = pearson(clients, rank_0, rank_1, alternative)
    return rho, p_value


def spearman_local(
    sample_0: list,
    sample_1: list,
    alternative: str = "less",
) -> Tuple[float, float]:
    return stats.spearmanr(sample_0, sample_1, alternative=alternative)
