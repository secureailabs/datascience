import math
from typing import Tuple

from sail_safe_functions.statistics.pearson_agregate import PearsonAgregate
from sail_safe_functions.statistics.pearson_precompute import PearsonPrecompute
from sail_safe_functions_orchestrator.series_federated import SeriesFederated
from scipy import stats
from scipy.stats import t



class PearsonFederate:
    """
    Computing the final Pearson Federated

    :return: _description_
    :rtype: _type_
    """

    @staticmethod
    def pearson(sample_0: SeriesFederated, sample_1: SeriesFederated, alternative: str) -> Tuple[float, float]:
        """
        This is the main Pearson function

        :param sample_0: _description_
        :type sample_0: SeriesFederated
        :param sample_1: _description_
        :type sample_1: SeriesFederated
        :return: single value r which is the pearson value

        """
        if alternative not in {"two-sided", "less", "greater"}:
            raise ValueError("alternative must be `two-sided`, `less` or `greater`")

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
        rho, degrees_of_freedom = PearsonAgregate.run(list_list_precompute)
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

    @staticmethod
    def run(sample_0: SeriesFederated, sample_1: SeriesFederated) -> Tuple[float, float]:
        return PearsonFederate.pearson(sample_0, sample_1, "two-sided")

    @staticmethod
    def run_reference(sample_0: SeriesFederated, sample_1: SeriesFederated) -> Tuple[float, float]:

        return stats.pearsonr(sample_0.to_numpy(), sample_1.to_numpy())
