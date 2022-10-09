from typing import Tuple

import numpy as np

from .clients import min_max_agg_client, min_max_client


def min_max(
    clients,
    sample_0: list,
) -> Tuple[float, float]:
    """
    Perform federated min max.
    It takes one federated series, and returns min and max value for it.

    :param sample_0: sample series
    :type sample_0: SeriesFederated
    :return: min and max value
    :rtype: Tuple[float, float]
    """
    list_list_precompute = []
    # TODO deal with posibilty sample_0 and sample_1 do not share same child frames

    # Calculating precompute
    for i in range(len(sample_0)):  # TODO replace these
        list_list_precompute.append(min_max_client(clients[i], sample_0[i]))

    # Final min max values
    min, max = min_max_agg_client(clients[0], list_list_precompute)
    return min, max


def min_max_local(
    sample_0: list,
) -> Tuple[float, float]:
    min_numpy = np.min(sample_0)  # TODO this is ugly as fuck
    max_numpy = np.max(sample_0)
    return min_numpy, max_numpy
