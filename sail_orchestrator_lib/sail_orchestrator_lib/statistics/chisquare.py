from typing import List

import numpy as np
import pandas as pd
from scipy import stats

from .clients import chisquare_agg_client, chisquare_client


def chisquare(
    clients,
    sample_0: List,
    sample_1: List,
):
    """
    chi square test

    :param clients: operating client
    :type clients: ZeroClient
    :param sample_0: sample 1
    :type sample_0: SeriesFederated
    :param sample_1: sample 2
    :type sample_1: SeriesFederated
    :return: chi square statistics and p value
    :rtype: tuple

    """

    precompute = []
    for i, client in enumerate(clients):
        res = chisquare_client(clients[i], sample_0[i], sample_1[i])
        precompute.append(res)
    return chisquare_agg_client(clients[0], precompute)


def chisquare_local(
    sample_0: pd.Series,
    sample_1: pd.Series,
):
    """
    obtain corresponding chi square test results from local scipy compute

    :param sample_0: sample 0
    :type sample_0: pd.Series
    :param sample_1: sample 1
    :type sample_1: pd.Series
    :return: chi square statistics and p value
    :rtype: tuple
    """
    count_total = sample_0.size

    array_0 = list(sample_0)
    array_1 = list(sample_1)
    list_unique_0 = np.unique(array_0).tolist()
    list_unique_1 = np.unique(array_1).tolist()
    array_true = np.zeros((len(list_unique_0), len(list_unique_1)))
    array_pred = np.zeros((len(list_unique_0), len(list_unique_1)))

    for i in range(len(array_0)):
        index_0 = list_unique_0.index(array_0[i])
        index_1 = list_unique_1.index(array_1[i])
        array_true[index_0, index_1] += 1

    for i_0 in range(len(list_unique_0)):
        for i_1 in range(len(list_unique_1)):
            array_pred[i_0, i_1] = array_true[i_0, :].sum() * array_true[:, i_1].sum() / count_total

    ddof = -((len(list_unique_0) - 1) * (len(list_unique_1) - 1)) + (len(array_true.ravel()) - 1)  # 2d instead of 1d
    chisquare_statistic, p_value = stats.chisquare(array_true.ravel(), f_exp=array_pred.ravel(), ddof=ddof)
    return chisquare_statistic, p_value
