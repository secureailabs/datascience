from sail_safe_functions_orchestrator.statistics.clients import student_t_agg_client, unpaired_t_client
from scipy import stats
from scipy.stats import t


def student_t(
    clients,
    sample_0: list,
    sample_1: list,
    alternative: str = "less",
):
    """
    It takes two federated series, and returns the p-value and t-statistics

    :param sample_0: First sample series
    :type sample_0: SeriesFederated
    :param sample_1: Second sample series
    :type sample_1: SeriesFederated
    :return: t_statistic, p_value
    :rtype: float, float
    """
    list_list_precompute = []
    # TODO deal with posibilty sample_0 and sample_1 do net share same child frames
    for i in range(len(sample_0)):
        list_list_precompute.append(
            unpaired_t_client(
                clients[i],
                sample_0[i],
                sample_1[i],
            )
        )

    t_statistic, degrees_of_freedom = student_t_agg_client(clients[0], list_list_precompute)
    p_value = t.cdf(t_statistic, degrees_of_freedom)
    if alternative == "less":
        p_value = t.cdf(t_statistic, degrees_of_freedom)
    elif alternative == "two-sided":
        p_value = t.cdf(t_statistic, degrees_of_freedom) / 2
    elif alternative == "greater":
        p_value = 1 - t.cdf(t_statistic, degrees_of_freedom)
    else:
        raise ValueError()
    return t_statistic, p_value


def student_t_local(
    sample_0: list,
    sample_1: list,
    alternative: str = "less",
):
    return stats.ttest_ind(
        sample_0.to_numpy(),
        sample_1.to_numpy(),
        equal_var=True,
        alternative=alternative,
    )
