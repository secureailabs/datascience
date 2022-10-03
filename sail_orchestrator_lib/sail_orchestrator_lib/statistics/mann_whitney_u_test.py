from typing import Tuple

import numpy
import scipy
from sail_orchestrator_lib.data import utils
from scipy import stats

from .clients import mann_whitney_agg_client, mann_whitney_client


def mann_whitney(
    clients,
    sample_0: list,
    sample_1: list,
    alternative: str = "less",
    type_ranking: str = "unsafe",
) -> Tuple[float, float]:
    """
    It takes two federated series, and returns the p-value and test statistic of the mann whitney u test
    Federated version of the mann whiney u test, it makes two compromised
    1. Tie correction was removed, it has a small impact most of the time. The reference implementation still does this.
    2. The p values is always computed asymptotoicly, exact methods is only feasable for small smalle sizes.

    :param sample_0: First sample series
    :type sample_0: SeriesFederated
    :param sample_1: Two sample series
    :type sample_1: SeriesFederated
    :return: _description_
    :rtype: Tuple[float, float]
    """
    n0 = 0
    n1 = 0
    for i in range(len(sample_0)):
        n0 += sample_0[i].size
        n1 += sample_1[i].size

    sample_concatenated = utils.fed_concat(clients, sample_0, sample_1)
    sample_concatenated_ranked = utils.rank_cdf(clients, sample_concatenated)

    list_precompute = []
    for i in range(len(sample_0)):
        list_precompute.append(mann_whitney_client(clients[i], sample_0[i], sample_concatenated_ranked[i]))

    sum_ranks_0 = mann_whitney_agg_client(clients[0], list_precompute)

    U0 = sum_ranks_0 - n0 * (n0 + 1) / 2
    U1 = n0 * n1 - U0

    mean = ((n0 * n1) + 1) / 2
    standard_deviation = numpy.sqrt(n0 * n1 / 12 * ((n0 + n1 + 1)))
    if alternative == "two-sided":
        U = numpy.maximum(U0, U1)
    elif alternative == "greater":
        U = U0
    elif alternative == "less":
        U = U1
    else:
        raise Exception

    z = (U - mean) / standard_deviation
    p = scipy.stats.norm.sf(z)
    if alternative == "two-sided":
        p *= 2

    # Ensure that test statistic is not greater than 1
    # This could happen for exact test when U = m*n/2
    p = numpy.clip(p, 0, 1)

    return U0, p


def mann_whitney_local(
    sample_0: list,
    sample_1: list,
    alternative: str = "less",
):
    return stats.mannwhitneyu(
        sample_0,
        sample_1,
        alternative=alternative,
        method="asymptotic",
    )
