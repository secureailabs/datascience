from typing import Tuple

from sail_safe_functions.aggregator.series_federated import SeriesFederated
from sail_safe_functions.aggregator.statistics.estimator import Estimator
from sail_safe_functions.participant.statistics.unpaired_t_test_precompute import UnpairedTTestPrecompute
from sail_safe_functions.participant.statistics.welch_t_test_aggregate import WelchTTestAggregate
from scipy import stats
from scipy.stats import t


def welch_t_test(
    sample_0: SeriesFederated,
    sample_1: SeriesFederated,
    alternative: str = "less",
) -> Tuple[float, float]:
    estimator = WelchTTest(alternative)
    return estimator.run(sample_0, sample_1)


class WelchTTest(Estimator):
    """
    This class contains method for federated Welch T test
    """

    def __init__(self, alternative) -> None:
        super().__init__(["t_statistic", "p_value"])
        if alternative not in ["less", "two-sided", "greater"]:
            raise ValueError('Alternative must be of "less", "two-sided" or "greater"')
        self.alternative = alternative

    def run(self, sample_0: SeriesFederated, sample_1: SeriesFederated):
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
        # TODO deal with posibilty sample_0 and sample_1 do net share same child frames
        for dataset_id in sample_0.list_dataset_id:
            client = sample_0.service_client.get_client(dataset_id)
            reference_series_0 = sample_0.get_reference_series(dataset_id)
            reference_series_1 = sample_1.get_reference_series(dataset_id)
            list_list_precompute.append(
                client.call(
                    UnpairedTTestPrecompute,
                    reference_series_0,
                    reference_series_1,
                )
            )

        t_statistic, degrees_of_freedom = WelchTTestAggregate.run(list_list_precompute)
        p_value = t.cdf(t_statistic, degrees_of_freedom)
        if self.alternative == "less":
            p_value = t.cdf(t_statistic, degrees_of_freedom)
        elif self.alternative == "two-sided":
            p_value = t.cdf(t_statistic, degrees_of_freedom) / 2
        elif self.alternative == "greater":
            p_value = 1 - t.cdf(t_statistic, degrees_of_freedom)
        else:
            raise ValueError()
        return t_statistic, p_value

    def run_reference(self, sample_0: SeriesFederated, sample_1: SeriesFederated):
        return stats.ttest_ind(
            sample_0.to_numpy(),
            sample_1.to_numpy(),
            equal_var=False,
            alternative=self.alternative,
        )
