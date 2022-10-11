import numpy as np
from sail_safe_functions_orchestrator.statistics.clients import variance_agg_client, variance_client


def variance(
    clients,
    sample_0: list,
):
    """
    It takes one federated series, and returns the variance of the series

    :param sample_0: _description_
    :type sample_0: SeriesFederated
    :return: _description_
    :rtype: _type_
    """
    list_list_precompute = []
    for i in range(len(sample_0)):
        list_list_precompute.append(variance_client(clients[i], sample_0[i]))
    variance = variance_agg_client(clients[0], list_list_precompute)
    return variance


def variance_local(
    sample_0: np.ndarray,
):
    return np.var(sample_0, ddof=1)
