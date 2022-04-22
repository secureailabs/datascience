from typing import Tuple
from sail_safe_functions_orchestrator.series_federated import SeriesFederated
from sail_safe_functions.statistics.unpaired_t_test_precompute import UnpairedTTestPrecompute
from sail_safe_functions.statistics.unpaired_t_test_agregate import UnpairedTTestAgregate

from scipy.stats import t


class UnpairedTTestFederate:
    @staticmethod
    def ttest_ind(
        sample_0: SeriesFederated,
        sample_1: SeriesFederated,
        equal_varriances: bool = False,
        alternative: str = "less",
    ) -> Tuple[float, float]:
        if alternative not in ["less", "two-sided", "greater"]:
            raise ValueError('Alternative must be of "less", "two-sided" or "greater"')

        list_list_precompute = []
        list_key_dataframe = list(sample_0.dict_series.keys())
        # TODO deal with posibilty sample_0 and sample_1 do net share same child frames
        for key_dataframe in list_key_dataframe:
            list_list_precompute.append(
                UnpairedTTestPrecompute.run(sample_0.dict_series[key_dataframe], sample_1.dict_series[key_dataframe])
            )

        t_statistic, degrees_of_freedom = UnpairedTTestAgregate.run(list_list_precompute, equal_varriances)
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
