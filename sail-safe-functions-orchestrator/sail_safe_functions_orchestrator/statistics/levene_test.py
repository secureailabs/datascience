from typing import Tuple

from sail_safe_functions.statistics.levene_aggregate import LeveneAggregate
from sail_safe_functions.statistics.levene_precompute import LevenePrecompute
from sail_safe_functions_orchestrator import statistics
from sail_safe_functions_orchestrator.series_federated import SeriesFederated
from sail_safe_functions_orchestrator.statistics.estimator import Estimator
from scipy import stats
from scipy.stats import distributions


def levene_test(
    sample_0: SeriesFederated,
    sample_1: SeriesFederated,
) -> Tuple[float, float]:
    """
    Perform federated Levene test for equal variances.

    Definition
    -----------
    The Levene test tests the null hypothesis that all input samples
    are from populations with equal variances.  Levene's test is an
    alternative to Bartlett's test `bartlett` in the case where
    there are significant deviations from normality.

    In statistics, Levene’s test is an inferential statistic used to
    evaluate the equality of variances for a variable determined for two
    or more groups. Some standard statistical procedures find that variances
    of the populations from which various samples are formed are equal.
    Levene’s test assesses this assumption. It examines the null hypothesis
    that the population variances are equal called homogeneity of variance or
    homoscedasticity. It compares the variances of k samples, where k can be more
    than two samples.
    It’s an alternative to Bartlett’s test that is less sensitive to
    departures from normality.
    There are several solutions to test for the equality (homogeneity)
    of variance across groups, including:

    -F-test
    -Bartlett’s test
    -Levene’s test
    -Fligner-Killeen test

    Examples
    --------
    Test whether or not the lists `a`, `b` and `c` come from populations
    with equal variances.

    >>> from sail_safe_functions_orchestrator.statistics.levene_test import LeveneTest
    >>> from sail_safe_functions_test.helper_sail_safe_functions.series_federated_local import SeriesFederatedLocal

    >>> sample_0 = SeriesFederatedLocal("sample_0")
    >>> sample_0.add_array("array_test", np.array([17.2, 20.9, 22.6, 18.1, 21.7, 21.4, 23.5,]) )
    >>> sample_1 = SeriesFederatedLocal("sample_1")
    >>> sample_1.add_array("array_test", np.array([21.5, 22.8, 21.0, 23.0, 21.6, 23.6, 22.5,]))

    >>> estimator = LeveneTest()
    >>> f_statistic_sail, p_value_sail = estimator.run(sample_0, sample_1)

    The small p-value suggests that the populations do not have equal
    variances.
    This is not surprising, given that the sample variance of `b` is much
    larger than that of `a` and `c`:

    References
    -----------
    ..[1] https://en.wikipedia.org/wiki/Levene%27s_test
    ..[2] https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.levene.html

    :param sample_0: fedrated series
    :type sample_0: SeriesFederated
    :param sample_1: _description_
    :type sample_1:  fedrsated series
    :return: F-stat, p-value
    :rtype: Tuple[float, float]

    """
    estimator = LeveneTest()
    return estimator.run(sample_0, sample_1)


class LeveneTest(Estimator):
    """
    This class contains the federated Levenes method

    :return: f_statistic(statistics from levenes test)  , p-value
    :rtype: float
    """

    def __init__(self) -> None:
        super().__init__(["f_statistic", "p_value"])

    def run(self, sample_0: SeriesFederated, sample_1: SeriesFederated):
        mean_sample_0 = statistics.mean(sample_0)
        mean_sample_1 = statistics.mean(sample_1)

        list_list_precompute = []
        list_key_dataframe = list(sample_0.dict_series.keys())
        # TODO deal with posibilty sample_0 and sample_1 do net share same child frames
        for key_dataframe in list_key_dataframe:
            list_list_precompute.append(
                LevenePrecompute.run(
                    sample_0.dict_series[key_dataframe],
                    sample_1.dict_series[key_dataframe],
                    mean_sample_0,
                    mean_sample_1,
                )
            )

        f_statistic, dof = LeveneAggregate.run(list_list_precompute)
        p_value = distributions.f.sf(f_statistic, 1, dof)  # 1 - cdf
        return f_statistic, p_value

    def run_reference(self, sample_0: SeriesFederated, sample_1: SeriesFederated):
        return stats.levene(sample_0.to_numpy(), sample_1.to_numpy(), center="mean")
