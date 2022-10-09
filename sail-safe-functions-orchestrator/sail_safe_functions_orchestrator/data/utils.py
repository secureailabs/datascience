from typing import List, Tuple

from sail_safe_functions_orchestrator.statistics import min_max

# def load_schema(client, path):
#     """
#     load a json schema as non secret object from client

#     :param client: operate client
#     :type client: ZeroClient
#     :param path: path of Json on remote machine
#     :type path: str
#     :return: load json in bytes
#     :rtype: bytes
#     """
#     return client.call("load_json", path)


def load_df_from_csv(client, path):
    """
    Load df from a csv file on the remote machine as a secret object

    :param client: operate client
    :type client: ZeroClient
    :param path: path of the csv on remote machine
    :type path: str
    :return: load df as secret object
    :rtype: SecretObject
    """
    rdf = client.call("load_df_from_csv", path)
    return rdf


def array(client, obj):
    """
    create a remote numpy array

    :param client: operate client
    :type client: ZeroClient
    :param obj: raw list data
    :type obj: list
    """
    rarr = client.call("array", obj)
    return rarr


def random_normal(client, loc=0.0, scale=1.0, size=None, seed=42):
    """
    create a random array follow normal distribution

    :param loc: mu, defaults to 0.0
    :type loc: float, optional
    :param scale: sigma, defaults to 1.0
    :type scale: float, optional
    :param size: size of 1d array, defaults to None
    :type size: int, optional
    :param seed: random seed, defaults to 42
    :type seed: int, optional
    """
    rarr = client.call("random_normal", loc, scale, size, seed)
    return rarr


def cdf_client(
    client,
    series,
    domain_min,
    domain_max,
):
    res = client.call("cdf", series, domain_min, domain_max)
    return res


def cdf_agg_client(
    client,
    list_precompute,
    domain_min,
    domain_max,
):
    res = client.call("cdf_agg", list_precompute, domain_min, domain_max)
    return res


def cdf_rank_client(
    client,
    sample_0,
    size_sample_total,
    list_domain_cdf,
    list_value_cdf,
):
    return client.call("cdf_rank", sample_0, size_sample_total, list_domain_cdf, list_value_cdf)


def cdf(
    clients: list,
    sample_0: list,
) -> Tuple[List[float], List[float]]:

    domain_min, domain_max = min_max(clients, sample_0)

    list_precompute = []
    for i in range(len(sample_0)):  # TODO rework abcs
        list_precompute.append(cdf_client(clients[i], sample_0[i], domain_min, domain_max))
    return cdf_agg_client(clients[0], list_precompute, domain_min, domain_max)


def rank_cdf(
    clients,
    sample_0: list,
):
    list_domain_cdf, list_value_cdf = cdf(clients, sample_0)
    sample_ranked_0 = []
    size_sample_0 = 0
    for sample in sample_0:
        size_sample_0 += sample.size
    for i in range(len(sample_0)):
        sample_ranked_0.append(
            cdf_rank_client(clients[i], sample_0[i], size_sample_0, list_domain_cdf, list_value_cdf),
        )
    return sample_ranked_0


def concat_client(
    client,
    obj1,
    obj2,
    axis=0,
    join="outer",
    ignore_index=False,
    keys=None,
    levels=None,
    names=None,
    verify_integrity=False,
    sort=False,
    copy=True,
):
    return client.call(
        "concat",
        obj1,
        obj2,
        axis,
        join,
        ignore_index,
        keys,
        levels,
        names,
        verify_integrity,
        sort,
        copy,
    )


def fed_concat(
    clients,
    objs1,
    objs2,
    axis=0,
    join="outer",
    ignore_index=False,
    keys=None,
    levels=None,
    names=None,
    verify_integrity=False,
    sort=False,
    copy=True,
):
    res = []
    for i in range(len(objs1)):
        res.append(
            concat_client(
                clients[i],
                objs1[i],
                objs2[i],
                axis,
                join,
                ignore_index,
                keys,
                levels,
                names,
                verify_integrity,
                sort,
                copy,
            )
        )
    return res


def wilcoxon_singed_rank_test_difference_tranform(
    sample_0: list,
    sample_1: list,
) -> Tuple[List[float], List[float]]:

    sample_difference = []
    sample_difference_absolute = []
    for i in range(len(sample_0)):
        series_0 = sample_0[i]
        series_1 = sample_1[i]
        series_difference = series_0.sub(series_1)
        series_difference_absolute = series_difference.abs()
        sample_difference.append(series_difference)
        sample_difference_absolute.append(series_difference_absolute)

    return sample_difference, sample_difference_absolute


def train_test_split_client(
    client,
    X,
    y,
    test_size,
    train_size,
    random_size,
    shuffle,
    stratify,
):
    return client.call("train_test_split", X, y, test_size, train_size, random_size, shuffle, stratify)


def train_test_split(
    Xs,
    ys,
    test_size=None,
    train_size=None,
    random_state=None,
    shuffle=True,
    stratify=None,
):
    X_train = []
    X_test = []
    y_train = []
    y_test = []

    if len(Xs) != len(ys):
        raise Exception("X and y must have equal length")

    for i in range(len(Xs)):
        Xtr, Xte, ytr, yte = train_test_split_client(
            Xs[i], ys[i], test_size, train_size, random_state, shuffle, stratify
        )
        X_train.append(Xtr)
        X_test.append(Xte)
        y_train.append(ytr)
        y_test.append(yte)

    return X_train, X_test, y_train, y_test
