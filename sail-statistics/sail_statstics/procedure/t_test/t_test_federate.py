from typing import Tuple
from sail_statstics.local_federated_dataframe import LocalFederatedDataframe

from sail_statstics.procedure.t_test.t_test_precompute import TTestPrecompute
from sail_statstics.procedure.t_test.t_test_agregate import TTestAgregate

from scipy.stats import t


class TTestFederate:
    @staticmethod
    def ttest_ind(
        sample_0: LocalFederatedDataframe,
        sample_1: LocalFederatedDataframe,
        equal_varriances: bool = False,
        alternative: str = "less",
    ) -> Tuple[float, float]:
        if 1 != len(sample_0.columns):
            raise ValueError("sample_0 must have exactly 1 comlumn")
        if 1 != len(sample_1.columns):
            raise ValueError("sample_1 must have exactly 1 comlumn")
        if alternative not in ["less", "two-sided", "greater"]:
            raise ValueError('Alternative must be of "less", "two-sided" or "greater"')

        list_list_precompute = []
        list_key_dataframe = list(sample_0.dict_dataframe.keys())
        # TODO deal with posibilty sample_0 and sample_1 do net share same child frames
        for key_dataframe in list_key_dataframe:
            list_list_precompute.append(
                TTestPrecompute.run(sample_0.dict_dataframe[key_dataframe], sample_1.dict_dataframe[key_dataframe])
            )

        t_statistic, degrees_of_freedom = TTestAgregate.run(list_list_precompute, equal_varriances)
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
