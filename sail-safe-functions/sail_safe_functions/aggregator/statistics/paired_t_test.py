from typing import List, Tuple

import numpy as np
from sail_core.implementation_manager import ImplementationManager
from sail_safe_functions.aggregator.series_federated import SeriesFederated
from sail_safe_functions.aggregator.statistics.estimator_two_sample import EstimatorTwoSample
from sail_safe_functions.aggregator.tools_common import check_variance_zero
from sail_safe_functions.participant.statistics.paired_t_test_precompute import PairedTTestPrecompute
from scipy import stats
from scipy.stats import t


def paired_t_test(
    sample_0: SeriesFederated,
    sample_1: SeriesFederated,
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
    >>> from sail_safe_functions.aggregator.statistics.student_t_test import StudentTTest
    >>> from sail_safe_functions.test.helper_sail_safe_functions.series_federated_local import SeriesFederatedLocal

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

    estimator = PairedTTest(alternative)
    return estimator.run(sample_0, sample_1)


class PairedTTest(EstimatorTwoSample):
    """
    PairedTTest this is the orchestator class that preforms a federated t-test
    """

    def __init__(
        self,
        alternative: str,
    ) -> None:
        super().__init__(f"PairedTTest - {alternative}", ["t_statistic", "p_value"])
        if alternative not in ["less", "two-sided", "greater"]:
            raise ValueError('Alternative must be of "less", "two-sided" or "greater"')
        self.alternative = alternative

    def run(self, sample_0: SeriesFederated, sample_1: SeriesFederated) -> Tuple[float, float]:
        list_list_precompute = []
        # TODO deal with posibilty sample_0 and sample_1 do not share same child frames: check indexes are the same

        participant_service = ImplementationManager.get_instance().get_participant_service()
        for dataset_id in sample_0.list_dataset_id:
            reference_series_0 = sample_0.get_reference_series(dataset_id)
            reference_series_1 = sample_1.get_reference_series(dataset_id)
            list_list_precompute.append(
                participant_service.call(
                    dataset_id,
                    PairedTTestPrecompute,
                    reference_series_0,
                    reference_series_1,
                )
            )

        t_statistic, degrees_of_freedom = self.aggregate(list_list_precompute)
        if self.alternative == "less":
            p_value = t.cdf(t_statistic, degrees_of_freedom)
        elif self.alternative == "two-sided":
            p_value = t.cdf(t_statistic, degrees_of_freedom) / 2
        elif self.alternative == "greater":
            p_value = 1 - t.cdf(t_statistic, degrees_of_freedom)
        else:
            raise ValueError()
        return t_statistic, p_value

    def aggregate(self, list_list_precompute: List[List[float]]) -> Tuple[float, float]:
        """collects the parts of a t-test and aggregates them into statisitcs

        :param list_list_precompute: a list of 3 floats; two moments for sample_d followed by the size of paired sample
        :type list_list_precompute: List[List[float]]
        :return: returns a t-statistic and its effect size
        :rtype: Tuple[float, float]
        """

        sum_d_0 = 0
        sum_dd_0 = 0
        size_sample_d = 0

        for list_precompute in list_list_precompute:
            sum_d_0 += list_precompute[0]
            sum_dd_0 += list_precompute[1]
            size_sample_d += list_precompute[2]

        sample_mean_d = sum_d_0 / size_sample_d
        sample_variance_d = ((sum_dd_0 / size_sample_d) - (sample_mean_d * sample_mean_d)) * (
            size_sample_d / (size_sample_d - 1)  # unbiased estimator (numpy version is biased by default)
        )
        check_variance_zero(sample_variance_d)
        t_statistic = sample_mean_d / (np.sqrt(sample_variance_d) / np.sqrt(size_sample_d))
        degrees_of_freedom = size_sample_d - 1

        # TODO we need to enable this when error handling is implemented
        # if degrees_of_freedom < 20:
        #     raise Exception()
        return t_statistic, degrees_of_freedom

    def run_reference(self, sample_0: SeriesFederated, sample_1: SeriesFederated) -> Tuple[float, float]:
        return stats.ttest_rel(sample_0.to_numpy(), sample_1.to_numpy(), alternative=self.alternative)
