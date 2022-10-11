from typing import Tuple

import numpy as np
from sail_safe_functions_orchestrator.data import utils
from sail_safe_functions_orchestrator.statistics.clients import kolmogorov_smirnov_agg_client, kolmogorov_smirnov_client
from sail_safe_functions_orchestrator.statistics.mean import mean
from sail_safe_functions_orchestrator.statistics.variance import variance
from scipy import stats
from scipy.stats import kstwo


def kolmogorov_smirnov(
    clients,
    sample_0: list,
    type_distribution="normal",
) -> Tuple[float, float]:
    """
    Perform federated kolmogorov_smirnov test.
    Executes a kolmogorov_smirnov test checking if sample 0 follows the given distribution.

    :param sample_0: sample to be tested
    :type sample_0: list
    :param type_distribution: type of ranking employed
    :type type_distribution: str
    :param type_ranking: type of rankign employed
    :type type_ranking: str
    :return: returns the k-statistic and the p-value
    :rtype: Tuple[float, float]
    """

    if type_distribution == "normal":
        sample_mean = mean(clients, sample_0)
        sample_standart_deviation = np.sqrt(variance(clients, sample_0))
        distribution = {
            "type_distribution": type_distribution,
            "sample_mean": sample_mean,
            "sample_standart_deviation": sample_standart_deviation,
        }
    elif type_distribution == "normalunit":
        distribution = {"type_distribution": type_distribution}
    else:
        raise Exception()

    size_sample = 0
    for sample in sample_0:
        size_sample += sample.size

    series_sample_ranked_0 = utils.rank_cdf(clients, sample_0)
    list_list_precompute = []
    for i in range(len(sample_0)):
        list_list_precompute.append(
            kolmogorov_smirnov_client(clients[i], sample_0[i], series_sample_ranked_0[i], distribution, size_sample)
        )
    k_statistic = kolmogorov_smirnov_agg_client(clients[0], list_list_precompute)

    p_value = kstwo.sf(k_statistic, size_sample)

    return k_statistic, p_value


def kolmogorov_smirnov_local(
    sample_0: list,
    type_distribution="normal",
) -> Tuple[float, float]:
    """
    local version of ks test, using scipy kstest function

    :param sample_0: sample 0
    :type sample_0: list
    :param type_distribution: distribution type, defaults to "normal"
    :type type_distribution: str, optional
    :return: ks statistics
    :rtype: Tuple[float, float]
    """
    if type_distribution == "normalunit":
        return stats.kstest(sample_0, "norm")
    else:
        raise Exception()
