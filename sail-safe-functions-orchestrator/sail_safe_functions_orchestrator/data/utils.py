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
    """
    client side function of cdf

    :param client: client object
    :type client: zero.ZeroClient
    :param series: retmoe series
    :type series: RemoteSeries
    :param domain_min: min of the value domain
    :type domain_min: float
    :param domain_max: max of the value domain
    :type domain_max: float
    :return: cdf distribution
    :rtype: List
    """
    res = client.call("cdf", series, domain_min, domain_max)
    return res


def cdf_agg_client(
    client,
    list_precompute,
    domain_min,
    domain_max,
):
    """
    client side function of cdf aggregation from each party

    :param client: client object
    :type client: zero.ZeroClient
    :param list_precompute: list of cdf from different parties
    :type list_precompute: list
    :param domain_min: min of value domain
    :type domain_min: float
    :param domain_max: max of value domain
    :type domain_max: float
    :return: aggregated cdf
    :rtype: list
    """
    res = client.call("cdf_agg", list_precompute, domain_min, domain_max)
    return res


def cdf_rank_client(
    client,
    sample_0,
    size_sample_total,
    list_domain_cdf,
    list_value_cdf,
):
    """
    client function to compute ranked cdf

    :param client: client object
    :type client: zero.ZeroClient
    :param sample_0: remote sample
    :type sample_0: Remote series
    :param size_sample_total: remote sample total
    :type size_sample_total: list
    :param list_domain_cdf: domain cdf
    :type list_domain_cdf: list
    :param list_value_cdf: value cdf
    :type list_value_cdf: list
    :return: ranked cdf
    :rtype: list
    """
    return client.call("cdf_rank", sample_0, size_sample_total, list_domain_cdf, list_value_cdf)


def cdf(
    clients: list,
    sample_0: list,
) -> Tuple[List[float], List[float]]:
    """
    user interface to compute sample cdf

    :param clients: _description_
    :type clients: list
    :param sample_0: _description_
    :type sample_0: list
    :return: _description_
    :rtype: Tuple[List[float], List[float]]
    """

    domain_min, domain_max = min_max(clients, sample_0)

    list_precompute = []
    for i in range(len(sample_0)):  # TODO rework abcs
        list_precompute.append(cdf_client(clients[i], sample_0[i], domain_min, domain_max))
    return cdf_agg_client(clients[0], list_precompute, domain_min, domain_max)


def rank_cdf(
    clients,
    sample_0: list,
):
    """
    user interface to compute randed cdf

    :param clients: _description_
    :type clients: _type_
    :param sample_0: _description_
    :type sample_0: list
    :return: _description_
    :rtype: _type_
    """
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
    """
    client side function of series concatenation

    :param client: _description_
    :type client: _type_
    :param obj1: _description_
    :type obj1: _type_
    :param obj2: _description_
    :type obj2: _type_
    :param axis: _description_, defaults to 0
    :type axis: int, optional
    :param join: _description_, defaults to "outer"
    :type join: str, optional
    :param ignore_index: _description_, defaults to False
    :type ignore_index: bool, optional
    :param keys: _description_, defaults to None
    :type keys: _type_, optional
    :param levels: _description_, defaults to None
    :type levels: _type_, optional
    :param names: _description_, defaults to None
    :type names: _type_, optional
    :param verify_integrity: _description_, defaults to False
    :type verify_integrity: bool, optional
    :param sort: _description_, defaults to False
    :type sort: bool, optional
    :param copy: _description_, defaults to True
    :type copy: bool, optional
    :return: _description_
    :rtype: _type_
    """
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
    """
    federated series concatenation

    :param clients: _description_
    :type clients: _type_
    :param objs1: _description_
    :type objs1: _type_
    :param objs2: _description_
    :type objs2: _type_
    :param axis: _description_, defaults to 0
    :type axis: int, optional
    :param join: _description_, defaults to "outer"
    :type join: str, optional
    :param ignore_index: _description_, defaults to False
    :type ignore_index: bool, optional
    :param keys: _description_, defaults to None
    :type keys: _type_, optional
    :param levels: _description_, defaults to None
    :type levels: _type_, optional
    :param names: _description_, defaults to None
    :type names: _type_, optional
    :param verify_integrity: _description_, defaults to False
    :type verify_integrity: bool, optional
    :param sort: _description_, defaults to False
    :type sort: bool, optional
    :param copy: _description_, defaults to True
    :type copy: bool, optional
    :return: _description_
    :rtype: _type_
    """
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
    """
    suer interface for wilcoxonsignedrank test transform

    :param sample_0: _description_
    :type sample_0: list
    :param sample_1: _description_
    :type sample_1: list
    :return: _description_
    :rtype: Tuple[List[float], List[float]]
    """

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
    """
    client side function for train test split

    :param client: _description_
    :type client: _type_
    :param X: _description_
    :type X: _type_
    :param y: _description_
    :type y: _type_
    :param test_size: _description_
    :type test_size: _type_
    :param train_size: _description_
    :type train_size: _type_
    :param random_size: _description_
    :type random_size: _type_
    :param shuffle: _description_
    :type shuffle: _type_
    :param stratify: _description_
    :type stratify: _type_
    :return: _description_
    :rtype: _type_
    """
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
    """
    user interface for train_test_split

    :param Xs: _description_
    :type Xs: _type_
    :param ys: _description_
    :type ys: _type_
    :param test_size: _description_, defaults to None
    :type test_size: _type_, optional
    :param train_size: _description_, defaults to None
    :type train_size: _type_, optional
    :param random_state: _description_, defaults to None
    :type random_state: _type_, optional
    :param shuffle: _description_, defaults to True
    :type shuffle: bool, optional
    :param stratify: _description_, defaults to None
    :type stratify: _type_, optional
    :raises Exception: _description_
    :return: _description_
    :rtype: _type_
    """
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
