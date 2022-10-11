import numpy as np
from sail_safe_functions_orchestrator.statistics.clients import skewness_agg_client, skewness_client
from scipy import stats


def skewness(
    clients,
    sample_0: list,
):
    """
    It takes one federated series, and returns the skewness value of the series.

    :param sample_0: sample series
    :type sample_0: SeriesFederated
    :return: skewness value of series
    :rtype: float
    """
    list_list_precompute = []

    # TODO deal with posibilty sample_0 and sample_1 do net share same child frames

    # Calculating precompute
    for i in range(len(sample_0)):
        list_list_precompute.append(skewness_client(clients[i], sample_0[i]))

    # Final Skew Value
    skewness = skewness_agg_client(clients[0], list_list_precompute)
    return skewness


def skewness_local(sample_0: np.ndarray):
    return stats.skew(sample_0)
