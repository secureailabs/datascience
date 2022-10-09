import numpy as np

from .clients import mean_agg_client, mean_client


def mean(
    clients,
    sample_0: list,
):
    """
    It takes one federated series, and returns the Mean

    :param sample_0: _description_
    :type sample_0: SeriesFederated
    :return: _description_
    :rtype: _type_
    """
    list_list_precompute = []
    for i in range(len(sample_0)):
        list_list_precompute.append(mean_client(clients[i], sample_0[i]))
    mean_statistic = mean_agg_client(clients[0], list_list_precompute)
    return mean_statistic


def mean_local(
    sample_0: list,
):
    return np.mean(sample_0)
