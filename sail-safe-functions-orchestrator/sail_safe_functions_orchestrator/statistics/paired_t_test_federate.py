from typing import Tuple

from sail_safe_functions.statistics.paired_t_test_agregate import PairedTTestAgregate
from sail_safe_functions.statistics.paired_t_test_precompute import PairedTTestPrecompute
from sail_safe_functions_orchestrator.series_federated import SeriesFederated
from sail_safe_functions_orchestrator.statistics.estimator import Estimator
from scipy import stats
from scipy.stats import t


class PairedTTestFederate(Estimator):
    """
    PairedTTestFederate this is the orchestator class that preforms a faderated t-test
    """

    def __init__(self, alternative) -> None:
        super().__init__()
        if alternative not in ["less", "two-sided", "greater"]:
            raise ValueError('Alternative must be of "less", "two-sided" or "greater"')
        self.list_name_estimate = ["t_statistic", "p_value"]
        self.alternative = alternative

    def ttest_rel(
        sample_0: SeriesFederated,
        sample_1: SeriesFederated,
        alternative: str = "less",
    ) -> Tuple[float, float]:
        """Preforms a paired t-test

        :param sample_0
        :type sample_0: SeriesFederated
        :param sample_1
        :type sample_1: SeriesFederated
        :param alternative: alternative for the test, defaults to "less"
        :type alternative: str, optional
        :raises ValueError: Raises a value error if alternative is not either {"less", "two-sided", "greater"}
        :return: Returns a t-statistic and its p-value
        :rtype: Tuple[float, float]
        """
        estimator = PairedTTestFederate(alternative)
        return estimator.run(sample_0, sample_1)

    def run(self, sample_0: SeriesFederated, sample_1: SeriesFederated) -> Tuple[float, float]:
        list_list_precompute = []
        list_key_dataframe = list(sample_0.dict_series.keys())
        # TODO deal with posibilty sample_0 and sample_1 do net share same child frames
        for key_dataframe in list_key_dataframe:
            list_list_precompute.append(
                PairedTTestPrecompute.run(
                    sample_0.dict_series[key_dataframe],
                    sample_1.dict_series[key_dataframe],
                )
            )

        t_statistic, degrees_of_freedom = PairedTTestAgregate.run(list_list_precompute)
        if self.alternative == "less":
            p_value = t.cdf(t_statistic, degrees_of_freedom)
        elif self.alternative == "two-sided":
            p_value = t.cdf(t_statistic, degrees_of_freedom) / 2
        elif self.alternative == "greater":
            p_value = 1 - t.cdf(t_statistic, degrees_of_freedom)
        else:
            raise ValueError()
        return t_statistic, p_value

    def run_reference(
        self, sample_0: SeriesFederated, sample_1: SeriesFederated, alternative: str
    ) -> Tuple[float, float]:
        return stats.ttest_rel(sample_0.to_numpy(), sample_1.to_numpy(), alternative=alternative)
