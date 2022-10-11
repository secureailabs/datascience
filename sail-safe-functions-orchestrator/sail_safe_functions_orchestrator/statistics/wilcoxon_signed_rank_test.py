import numpy
import scipy
from sail_safe_functions_orchestrator.data import utils
from sail_safe_functions_orchestrator.statistics.clients import (
    wilcoxon_signed_rank_agg_client,
    wilcoxon_signed_rank_client,
)


def wilcoxon_signed_rank(
    clients,
    sample_0: list,
    sample_1: list,
    alternative="less",
):
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
    size_sample_0 = 0
    size_sample_1 = 0
    for i in range(len(sample_0)):
        size_sample_0 += sample_0[i].size
        size_sample_1 += sample_1[i].size

    if size_sample_0 != size_sample_1:
        raise ValueError("`sample_0` and `sample_1` must have the same length.")

    size_sample = size_sample_0
    sample_difference, sample_difference_absolute = utils.wilcoxon_singed_rank_test_difference_tranform(
        sample_0, sample_1
    )
    sample_difference_absolute_ranked = utils.rank_cdf(clients, sample_difference_absolute)

    # Calculating precompute
    list_precompute = []
    for i in range(len(sample_0)):
        list_precompute.append(
            wilcoxon_signed_rank_client(clients[i], sample_difference[i], sample_difference_absolute_ranked[i])
        )

    # rank_minus rank_plus
    rank_minus, rank_plus = wilcoxon_signed_rank_agg_client(clients[0], list_precompute)

    if alternative == "two-sided":
        w_statistic = min(rank_minus, rank_plus)
    else:
        w_statistic = rank_plus

    mean = size_sample * (size_sample + 1.0) * 0.25
    standard_deviation = numpy.sqrt(size_sample * (size_sample + 1.0) * (2.0 * size_sample + 1.0) / 24)
    z_statistic = (w_statistic - mean) / standard_deviation

    if alternative == "two-sided":
        p_value = 2.0 * scipy.stats.distributions.norm.sf(abs(z_statistic))
    elif alternative == "less":
        p_value = scipy.stats.distributions.norm.cdf(z_statistic)
    elif alternative == "greater":
        p_value = scipy.stats.distributions.norm.sf(z_statistic)
    else:
        raise Exception()

    return w_statistic, p_value


def wilcoxon_signed_rank_local(
    sample_0: list,
    sample_1: list,
    alternative: str = "less",
):
    # we only do aproximation of T(aproximation does not work very wel below 10) and only do wilcox mode tie resolution
    return scipy.stats.wilcoxon(
        sample_0,
        sample_1,
        zero_method="wilcox",
        alternative=alternative,
        mode="approx",
    )
