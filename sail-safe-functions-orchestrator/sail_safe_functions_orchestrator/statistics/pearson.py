import math
from typing import Tuple

from sail_safe_functions.statistics.pearson_aggregate import PearsonAggregate
from sail_safe_functions.statistics.pearson_precompute import PearsonPrecompute
from sail_safe_functions_orchestrator.series_federated import SeriesFederated
from sail_safe_functions_orchestrator.statistics.estimator import Estimator
from scipy import stats
from scipy.stats import t


def pearson(
    sample_0: SeriesFederated, sample_1: SeriesFederated, alternative: str
) -> Tuple[float, float]:
    """
    This is the main Pearson function

    :param sample_0: sample_0
    :type sample_0: SeriesFederated
    :param sample_1: sample_1
    :type sample_1: SeriesFederated
    :return: single value r which is the pearson value

    """
    estimator = Pearson(alternative)
    return estimator.run(sample_0, sample_1)


class Pearson(Estimator):
    """
    Estimator for pearson product
    """

    def __init__(self, alternative) -> None:
        super().__init__(["rho", "p_value"])
        if alternative not in ["less", "two-sided", "greater"]:
            raise ValueError('Alternative must be of "less", "two-sided" or "greater"')
        self.alternative = alternative

    def run(
        self, sample_0: SeriesFederated, sample_1: SeriesFederated
    ) -> Tuple[float, float]:
        """
        Run federated pearson function

        :param sample_0: _description_
        :type sample_0: SeriesFederated
        :param sample_1: _description_
        :type sample_1: SeriesFederated
        :raises ValueError: _description_
        :return: _description_
        :rtype: Tuple[float, float]
        """
        list_list_precompute = []
        list_key_dataframe = list(sample_0.dict_series.keys())
        # TODO deal with posibilty sample_0 and sample_1 do net share same child frames
        for key_dataframe in list_key_dataframe:
            list_list_precompute.append(
                PearsonPrecompute.run(
                    sample_0.dict_series[key_dataframe],
                    sample_1.dict_series[key_dataframe],
                )
            )
        rho, degrees_of_freedom = PearsonAggregate.run(list_list_precompute)
        t_statistic = rho * math.sqrt(degrees_of_freedom / (1 - rho**2))
        if self.alternative == "less":
            p_value = t.cdf(t_statistic, degrees_of_freedom)
        elif self.alternative == "two-sided":
            p_value = 2 - t.cdf(t_statistic, degrees_of_freedom) * 2
        elif self.alternative == "greater":
            p_value = 1 - t.cdf(t_statistic, degrees_of_freedom)
        else:
            raise ValueError()

        return rho, p_value

    def run_reference(
        self, sample_0: SeriesFederated, sample_1: SeriesFederated
    ) -> Tuple[float, float]:

        return stats.pearsonr(sample_0.to_numpy(), sample_1.to_numpy())
