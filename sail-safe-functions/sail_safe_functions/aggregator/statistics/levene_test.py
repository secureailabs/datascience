from typing import List, Tuple

import numpy as np
from sail_core.implementation_manager import ImplementationManager
from sail_safe_functions.aggregator import statistics
from sail_safe_functions.aggregator.series_federated import SeriesFederated
from sail_safe_functions.aggregator.statistics.estimator_two_sample import EstimatorTwoSample
from sail_safe_functions.participant.statistics.levene_precompute import LevenePrecompute
from scipy import stats
from scipy.stats import distributions


def levene_test(
    sample_0: SeriesFederated,
    sample_1: SeriesFederated,
) -> Tuple[float, float]:
    """
    Perform federated Levene test for equal variances.
    It takes two federated series, and returns the p-value and test statistic of the Levene test.

        :param sample_0: The first sample of data
        :type sample_0: SeriesFederated
        :param sample_1: The second sample of data
        :type sample_1:  federated series
        :return: F-stat, p-value
        :rtype: Tuple[float, float]


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

    >>> from sail_safe_functions.aggregator.statistics.levene_test import LeveneTest
    >>> from sail_safe_functions.test.helper_sail_safe_functions.series_federated_local import SeriesFederatedLocal

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


    """
    estimator = LeveneTest()
    return estimator.run(sample_0, sample_1)


class LeveneTest(EstimatorTwoSample):
    """
    This class contains the federated Levenes method

    :return: f_statistic(statistics from levenes test)  , p-value

    :rtype: float
    """

    def __init__(self) -> None:
        super().__init__("LeveneTest", ["f_statistic", "p_value"])

    def run(
        self,
        sample_0: SeriesFederated,
        sample_1: SeriesFederated,
    ) -> Tuple[float, float]:
        mean_sample_0 = statistics.mean(sample_0)
        mean_sample_1 = statistics.mean(sample_1)

        list_precompute = []
        # TODO deal with posibilty sample_0 and sample_1 do net share same child frames
        participant_service = ImplementationManager.get_instance().get_participant_service()
        for dataset_id in sample_0.list_dataset_id:
            list_precompute.append(
                participant_service.call(
                    dataset_id,
                    LevenePrecompute,
                    sample_0.dict_reference_series[dataset_id],
                    sample_1.dict_reference_series[dataset_id],
                    mean_sample_0,
                    mean_sample_1,
                )
            )

        f_statistic, dof = self.aggregate(list_precompute)
        p_value = distributions.f.sf(f_statistic, 1, dof)  # 1 - cdf
        return f_statistic, p_value

    def aggregate(
        self,
        list_list_precompute: List[List[float]],
    ) -> Tuple[float, float]:
        sum_x_0 = 0
        sum_xx_0 = 0
        size_sample_0 = 0
        sum_x_1 = 0
        sum_xx_1 = 0
        size_sample_1 = 0
        final_z1j = []
        final_z2j = []
        for list_precompute in list_list_precompute:
            sum_x_0 += list_precompute[0]
            sum_xx_0 += list_precompute[1]
            size_sample_0 += list_precompute[2]
            sum_x_1 += list_precompute[3]
            sum_xx_1 += list_precompute[4]
            size_sample_1 += list_precompute[5]
            final_z1j.extend(list_precompute[6])
            final_z2j.extend(list_precompute[7])

        z1_ = np.mean(final_z1j)
        z2_ = np.mean(final_z2j)

        z__ = (z1_ + z2_) / 2

        denomenator_1 = final_z1j - z1_
        denomenator_1 = np.sum(denomenator_1 * denomenator_1)

        denomenator_2 = final_z2j - z2_
        denomenator_2 = np.sum(denomenator_2 * denomenator_2)

        final_denomenator = denomenator_1 + denomenator_2
        length1 = size_sample_0
        length2 = size_sample_1
        dof = length1 + length2 - 2
        final_numerator = dof * (length1 * (z1_ - z__) * (z1_ - z__) + length2 * (z2_ - z__) * (z2_ - z__))

        f_statictic = final_numerator / final_denomenator

        return f_statictic, dof
