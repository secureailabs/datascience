from typing import List, Optional, Tuple, Type

import numpy as np
import pandas as pd
import scipy
from sklearn.model_selection import train_test_split as split
from zero import ProxyObject, SecretObject

from .dataframe import RemoteDataFrame
from .series import RemoteSeries
from .typing import ArrayLike, copy_doc


def cdf(
    sample_0: Type[RemoteSeries],
    domain_min: float,
    domain_max: float,
) -> Tuple[List[float], List[float], int]:
    """
    generate cdf with raw data

    :param sample_0: _description_
    :type sample_0: Type[RemoteSeries]
    :param domain_min: _description_
    :type domain_min: float
    :param domain_max: _description_
    :type domain_max: float
    :return: _description_
    :rtype: Tuple[List[float], List[float], int]
    """
    # TODO test this for series of size 1
    array_sample_0 = sample_0.series.to_numpy()
    size_sample_0 = len(array_sample_0)
    if size_sample_0 == 1:
        array_domain_safe = np.array([sample_0[0], sample_0[0]])
        array_value_safe = np.array([0, 1])
    else:
        count_value = int(np.ceil(np.sqrt(len(array_sample_0))))

        array_domain = np.sort(array_sample_0)
        array_domain = np.insert(array_domain, 0, domain_min)
        array_domain = np.insert(array_domain, -1, domain_max)
        array_value = np.arange(1, size_sample_0 + 1) / float(size_sample_0)
        array_value = np.insert(array_value, 0, 0)
        array_value = np.insert(array_value, -1, 1)

        array_domain_safe = np.linspace(domain_min, domain_max, count_value).tolist()
        array_value_safe = scipy.interpolate.interp1d(array_domain, array_value)(array_domain_safe)
        array_value_safe = array_value_safe.tolist()
    return [array_domain_safe, array_value_safe, size_sample_0]


def cdf_agg(
    list_precompute: List[Tuple[List[float], List[float], int]],
    domain_min: float,
    domain_max: float,
) -> Tuple[List[float], List[float]]:
    """
    aggreate cdf from different parties

    :param list_precompute: _description_
    :type list_precompute: List[Tuple[List[float], List[float], int]]
    :param domain_min: _description_
    :type domain_min: float
    :param domain_max: _description_
    :type domain_max: float
    :return: _description_
    :rtype: Tuple[List[float], List[float]]
    """
    list_array_value_resampled = []
    count_total = 0
    for precompute in list_precompute:
        count_total += precompute[2]
    count_value = int(np.ceil(np.sqrt(count_total)))

    array_domain_resampled = np.linspace(domain_min, domain_max, count_value)
    list_weight = []
    for precompute in list_precompute:
        precompute = list(precompute)
        list_weight.append(precompute[2] / count_total)
        precompute[0] = np.array(precompute[0])
        precompute[1] = np.array(precompute[1])
        list_array_value_resampled.append(
            scipy.interpolate.interp1d(precompute[0], precompute[1])(array_domain_resampled)
        )

    array_weight = np.array(list_weight)
    array_value_resampled = np.matmul(np.vstack(list_array_value_resampled).T, array_weight)

    return array_domain_resampled.tolist(), array_value_resampled.tolist()


def cdf_rank(
    sample_0: Type[RemoteSeries],
    size_sample_total: int,
    list_domain_cdf: List[float],
    list_value_cdf: List[float],
) -> list:
    """
    rank cdf from raw data

    :param sample_0: _description_
    :type sample_0: Type[RemoteSeries]
    :param size_sample_total: _description_
    :type size_sample_total: int
    :param list_domain_cdf: _description_
    :type list_domain_cdf: List[float]
    :param list_value_cdf: _description_
    :type list_value_cdf: List[float]
    :return: _description_
    :rtype: list
    """
    array_sample_0 = sample_0.series.to_numpy()
    function_cdf = scipy.interpolate.interp1d(np.array(list_domain_cdf), np.array(list_value_cdf))
    array_rank = np.round(function_cdf(array_sample_0) * size_sample_total)
    return array_rank.tolist()


def load_df_from_csv(
    path: str,
) -> Type[ProxyObject]:
    """
    load dataframe from csv file

    :param path: csv file path
    :type path: str
    :return: dataframe as proxy object
    :rtype: Type[ProxyObject]
    """
    df = pd.read_csv(path)
    df = RemoteDataFrame(d=df)
    return ProxyObject(df)


@copy_doc(pd.concat)
def concat(
    obj1: Type[RemoteSeries],
    obj2: Type[RemoteSeries],
    axis: int = 0,
    join: str = "outer",
    ignore_index: bool = False,
    keys: Optional[list] = None,
    levels: Optional[list] = None,
    names: Optional[list] = None,
    verify_integrity: bool = False,
    sort: bool = False,
    copy: bool = True,
) -> Type[ProxyObject]:
    ans = pd.concat([obj1.series, obj2.series])
    ans = RemoteSeries(d=ans)
    return ProxyObject(ans)


@copy_doc(split)
def train_test_split(
    *arrays: ArrayLike,
    test_size: float = None,
    train_size: float = None,
    random_state: int = None,
    shuffle: bool = True,
    stratify: ArrayLike = None,
):
    X_train, X_test, y_train, y_test = split(*arrays, test_size, train_size, random_state, shuffle, stratify)
    # to do: dimension check
    X_train = RemoteDataFrame(d=X_train)
    X_test = RemoteDataFrame(d=X_test)
    y_train = RemoteSeries(d=y_train)
    y_test = RemoteSeries(d=y_test)
    return ProxyObject(X_train), ProxyObject(X_test), ProxyObject(y_train), ProxyObject(y_test)
