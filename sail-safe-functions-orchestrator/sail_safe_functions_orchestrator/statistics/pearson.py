import math
from typing import Tuple

from scipy import stats
from scipy.stats import t

from .clients import pearson_agg_client, pearson_client


def pearson(
    clients,
    sample_0: list,
    sample_1: list,
    alternative: str = "less",
) -> Tuple[float, float]:
    """
    Perform federated Pearson.
    It takes two federated series, and returns the rho value and the p-value
    ----------------
        :param sample_0: The first sample of data
        :type sample_0: SeriesFederated
        :param sample_1: The Second sample of data
        :type sample_1: SeriesFederated
        :return: two values pearson and p value

    In statistics, the Pearson correlation coefficient ― also known as Pearson's r,
    the Pearson product-moment correlation coefficient (PPMCC), the bivariate correlation, or colloquially
    simply as the correlation coefficient ― is a measure of linear correlation between two sets of data.
    It is the ratio between the covariance of two variables and the product of their standard
    deviations; thus, it is essentially a normalized measurement of the covariance, such that the result always
    has a value between −1 and 1. As with covariance itself, the measure can only reflect a linear correlation of variables,
    and ignores many other types of relationships or correlations. As a simple example, one would expect the age
    and height of a sample of teenagers from a high school to have a Pearson correlation coefficient significantly
    greater than 0, but less than 1 (as 1 would represent an unrealistically perfect correlation).
    ------------------

    Examples
    --------

    >>> from sail_safe_functions_orchestrator.statistics.pearson import Pearson
    >>> import numpy as np
    >>> from sail_safe_functions_test.helper_sail_safe_functions.series_federated_local import SeriesFederatedLocal

    >>> sample_0 = SeriesFederatedLocal("sample_0")
    >>> sample_0.add_array("array_test", np.array([17.2, 20.9, 22.6, 18.1, 21.7, 21.4, 23.5,]) )
    >>> sample_1 = SeriesFederatedLocal("sample_1")
    >>> sample_1.add_array("array_test", np.array([21.5, 22.8, 21.0, 23.0, 21.6, 23.6, 22.5,]))

    >>>
    >>>
    >>> estimator = Pearson(alternative=alternative)
    >>> pearson_sail, p_value_sail = estimator.run(sample_0, sample_1)


    There is a linear dependence between x and y if y = a + b*x + e, where
    a,b are constants and e is a random error term, assumed to be independent
    of x. For simplicity, assume that x is standard normal, a=0, b=1 and let
    e follow a normal distribution with mean zero and standard deviation s>0.


    References
    ----------
    .. [1] "Pearson correlation coefficient", Wikipedia,
        https://en.wikipedia.org/wiki/Pearson_correlation_coefficient
    .. [2] Student, "Probable error of a correlation coefficient",
        Biometrika, Volume 6, Issue 2-3, 1 September 1908, pp. 302-310.
    .. [3] C. J. Kowalski, "On the Effects of Non-Normality on the Distribution
        of the Sample Product-Moment Correlation Coefficient"
        Journal of the Royal Statistical Society. Series C (Applied
        Statistics), Vol. 21, No. 1 (1972), pp. 1-12.

    """
    list_list_precompute = []
    for i in range(len(sample_0)):
        list_list_precompute.append(
            pearson_client(
                clients[i],
                sample_0[i],
                sample_1[i],
            )
        )
    rho, degrees_of_freedom = pearson_agg_client(clients[0], list_list_precompute)
    t_statistic = rho * math.sqrt(degrees_of_freedom / (1 - rho**2))
    if alternative == "less":
        p_value = t.cdf(t_statistic, degrees_of_freedom)
    elif alternative == "two-sided":
        p_value = 2 - t.cdf(t_statistic, degrees_of_freedom) * 2
    elif alternative == "greater":
        p_value = 1 - t.cdf(t_statistic, degrees_of_freedom)
    else:
        raise ValueError()

    return rho, p_value


def pearson_local(sample_0, sample_1) -> Tuple[float, float]:

    return stats.pearsonr(sample_0.to_numpy(), sample_1.to_numpy())
