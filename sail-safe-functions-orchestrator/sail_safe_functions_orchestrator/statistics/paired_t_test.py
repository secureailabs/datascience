from typing import Tuple

from sail_safe_functions_orchestrator.statistics.clients import paired_t_agg_client, paired_t_client
from scipy import stats
from scipy.stats import t


def paired_t(
    clients,
    sample_0: list,
    sample_1: list,
    alternative: str = "less",
) -> Tuple[float, float]:
    """
    Perform federated paired t test.
    It takes two federated series, and returns the t-statistic and p-value for a paired t-test.

        :param sample_0: The first sample of data
        :type sample_0: SeriesFederated
        :param sample_1: The second sample of data
        :type sample_1: SeriesFederated
        :param alternative: alternative for the test, defaults to "less"
        :type alternative: str, optional
        :raises ValueError: Raises a value error if alternative is not either {"less", "two-sided", "greater"}
        :return: The t-statistic and the p-value.
        :rtype: Tuple[float, float]

    The paired t-test is a method used to test whether the mean difference between pairs of measurements is zero or not.
    You can use the test when your data values are paired measurements. For example, you might have before-and-after
    measurements for a group of people. Also, the distribution of differences between the paired measurements should be
    normally distributed.
    The paired t-test is also known as the dependent samples t-test, the paired-difference t-test, the matched pairs
    t-test and the repeated-samples t-test.
    If your sample sizes are very small, you might not be able to test for normality. You might need to rely on your
    understanding of the data. Or, you can perform a nonparametric test that doesn’t assume normality.

    Notes
    -----
    Examples for use are scores of the same set of student in
    different exams, or repeated sampling from the same units. The
    test measures whether the average score differs significantly
    across samples (e.g. exams). If we observe a large p-value, for
    example greater than 0.05 or 0.1 then we cannot reject the null
    hypothesis of identical average scores. If the p-value is smaller
    than the threshold, e.g. 1%, 5% or 10%, then we reject the null
    hypothesis of equal averages. Small p-values are associated with
    large t-statistics.

    Examples
    --------
    >>> from scipy import stats
    >>> from sail_safe_functions_orchestrator.statistics.student_t_test import StudentTTest
    >>> from sail_safe_functions_test.helper_sail_safe_functions.series_federated_local import SeriesFederatedLocal

    >>> sample_0 = SeriesFederatedLocal("sample_0")
    >>> sample_0.add_array("array_test", np.array([17.2, 20.9, 22.6, 18.1, 21.7, 21.4, 23.5,]) )
    >>> sample_1 = SeriesFederatedLocal("sample_1")
    >>> sample_1.add_array("array_test", np.array([21.5, 22.8, 21.0, 23.0, 21.6, 23.6, 22.5,]))


    >>> estimator = StudentTTest(alternative=alternative)
    >>> t_statistic_sail, p_value_sail = estimator.run(sample_0, sample_1)

    References
    ----------
    ..[1] https://en.wikipedia.org/wiki/T-test#Dependent_t-test_for_paired_samples
    """
    list_list_precompute = []
    # TODO deal with posibilty sample_0 and sample_1 do net share same child frames
    for i in range(len(sample_0)):
        list_list_precompute.append(
            paired_t_client(
                clients[i],
                sample_0[i],
                sample_1[i],
            )
        )

    t_statistic, degrees_of_freedom = paired_t_agg_client(clients[0], list_list_precompute)
    if alternative == "less":
        p_value = t.cdf(t_statistic, degrees_of_freedom)
    elif alternative == "two-sided":
        p_value = t.cdf(t_statistic, degrees_of_freedom) / 2
    elif alternative == "greater":
        p_value = 1 - t.cdf(t_statistic, degrees_of_freedom)
    else:
        raise ValueError()
    return t_statistic, p_value


def paired_t_local(
    sample_0: list,
    sample_1: list,
    alternative: str = "less",
) -> Tuple[float, float]:
    return stats.ttest_rel(sample_0, sample_1, alternative=alternative)
