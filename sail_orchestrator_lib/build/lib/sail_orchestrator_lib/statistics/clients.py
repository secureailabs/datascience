def chisquare_client(
    client,
    sample_0,
    sample_1,
):
    """
    RPC client side interface for chi square procompute

    :param client: operating client
    :type client: ZeroClient
    :param sample_0: sample 0
    :type sample_0: dict
    :param sample_1: sample 1
    :type sample_1: dict
    :return: precomputing result
    :rtype: list
    """
    return client.call("chisquare", sample_0, sample_1)


def chisquare_agg_client(
    client,
    list_precompute,
):
    """
    client side interface for chi square aggragation

    :param client: operating client
    :type client: ZeroClient
    :param list_precompute: precomputing results from different parties
    :type list_precompute: list
    :return: chi square statistics and p value
    :rtype: tuple
    """
    return client.call("chisquare_agg", list_precompute)


def kolmogorov_smirnov_client(
    client,
    sample_0,
    sample_ranked_0,
    distribution,
    count_total,
):
    return client.call("kolmogorov_smirnovdef", sample_0, sample_ranked_0, distribution, count_total)


def kolmogorov_smirnov_agg_client(
    client,
    list_precompute,
):
    return client.call("kolmogorov_smirnovdef_agg", list_precompute)


def kurtosis_client(
    client,
    sample_0_dataframe,
):
    return client.call("kurtosis", sample_0_dataframe)


def kurtosis_agg_client(
    client,
    list_list_precompute,
):
    return client.call("kurtosis_agg", list_list_precompute)


def levene_client(
    client,
    sample_0_series,
    sample_1_series,
    mean_0,
    mean_1,
):
    return client.call("levene", sample_0_series, sample_1_series, mean_0, mean_1)


def levene_agg_client(
    client,
    list_list_precompute,
    equal_varriances=False,
):
    return client.call("levene_agg", list_list_precompute, equal_varriances)


def mann_whitney_client(
    client,
    series_0,
    series_concatenated_ranked,
):
    return client.call("mann_whitney", series_0, series_concatenated_ranked)


def mann_whitney_agg_client(
    client,
    list_precompute,
):
    return client.call("mann_whitney_agg", list_precompute)


def mean_client(
    client,
    sample_0_dataframe,
):
    return client.call("mean", sample_0_dataframe)


def mean_agg_client(
    client,
    list_list_precompute,
):
    return client.call("mean_agg", list_list_precompute)


def min_max_client(
    client,
    series_sample,
):
    return client.call("min_max", series_sample)


def min_max_agg_client(
    client,
    list_tuple_min_max,
):
    return client.call("min_max_agg", list_tuple_min_max)


def paired_t_client(
    client,
    sample_0_series,
    sample_1_series,
):
    return client.call("paired_t", sample_0_series, sample_1_series)


def paired_t_agg_client(
    client,
    list_list_precompute,
):
    return client.call("paired_t_agg", list_list_precompute)


def pearson_client(
    client,
    sample_0_dataframe,
    sample_1_dataframe,
):
    return client.call("pearson", sample_0_dataframe, sample_1_dataframe)


def pearson_agg_client(
    client,
    list_list_precompute,
):
    return client.call("pearson_agg", list_list_precompute)


def skewness_client(
    client,
    sample_0_dataframe,
):
    return client.call("skewness", sample_0_dataframe)


def skewness_agg_client(
    client,
    list_list_precompute,
):
    return client.call("skewness_agg", list_list_precompute)


def unpaired_t_client(
    client,
    sample_0_series,
    sample_1_series,
):
    return client.call("unpaired_t", sample_0_series, sample_1_series)


def student_t_agg_client(
    client,
    list_list_precompute,
):
    return client.call("student_t_agg", list_list_precompute)


def variance_client(
    client,
    sample_0,
):
    return client.call("variance", sample_0)


def variance_agg_client(
    client,
    list_list_precompute,
):
    return client.call("variance_agg", list_list_precompute)


def welch_t_agg_client(
    client,
    list_list_precompute,
):
    return client.call("welch_t_agg", list_list_precompute)


def wilcoxon_signed_rank_client(
    client,
    sample_difference,
    sample_absolute_difference_ranked,
):
    return client.call("wilcoxon_signed_rank", sample_difference, sample_absolute_difference_ranked)


def wilcoxon_signed_rank_agg_client(
    client,
    list_precompute,
):
    return client.call("wilcoxon_signed_rank_agg", list_precompute)
