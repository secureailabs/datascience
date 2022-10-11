from sail_safe_functions_orchestrator.statistics.clients import unpaired_t_client, welch_t_agg_client
from scipy import stats
from scipy.stats import t


def welch_t(
    clients,
    sample_0: list,
    sample_1: list,
    alternative: str = "less",
):
    """
    Perform federated Welch T test.
    It takes two federated series, and returns the p-value and test statistic of the Levene test

    :param sample_0: First series sample
    :type sample_0: SeriesFederated
    :param sample_1: Second series sample
    :type sample_1: SeriesFederated
    :return: t_statistic, p_value
    :rtype: Float, Float
    """
    list_list_precompute = []
    for i in range(len(sample_0)):
        list_list_precompute.append(
            unpaired_t_client(
                clients[i],
                sample_0[i],
                sample_1[i],
            )
        )

    t_statistic, degrees_of_freedom = welch_t_agg_client(clients[0], list_list_precompute)
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


def welch_t_local(
    sample_0: list,
    sample_1: list,
    alternative: str = "less",
):
    return stats.ttest_ind(
        sample_0,
        sample_1,
        equal_var=False,
        alternative=alternative,
    )
