import imp
from sail_statstics.local_federated_dataframe import LocalFederatedDataframe

from sail_statstics.procedure.t_test_precompute import TTestPrecompute
from sail_statstics.procedure.t_test_agregate import TTestAgregate

from scipy.stats import t


class TTestFederate:
    @staticmethod
    def ttest_ind(
        sample_0: LocalFederatedDataframe,
        sample_1: LocalFederatedDataframe,
        equal_var: bool = True,
        alternative: str = "less",
    ):
        if not equal_var:
            raise NotImplementedError()

        list_list_precompute = []
        list_key_dataframe = list(sample_0.dict_dataframe.keys())
        # TODO deal with posibilty sample_0 and sample_1 do net share same child frames
        # TODO deal with posibilty sample_0 and sample_1 have more than 1 column
        for key_dataframe in list_key_dataframe:
            sample_0.dict_dataframe[key_dataframe]
            sample_1.dict_dataframe[key_dataframe]
            list_list_precompute.append(
                TTestPrecompute.run(sample_0.dict_dataframe[key_dataframe], sample_1.dict_dataframe[key_dataframe])
            )

        t_statistic, degrees_of_freedom = TTestAgregate.run(list_list_precompute)
        p_value = t.cdf(t_statistic, degrees_of_freedom)
        if alternative == "less":
            p_value = t.cdf(t_statistic, degrees_of_freedom)
        return t_statistic, p_value
