from typing import Tuple
from sail_statstics.local_federated_dataframe import LocalFederatedDataframe

from sail_statstics.procedure.skewness.skewness_precompute import SkewnessPrecompute
from sail_statstics.procedure.skewness.skewness_agregate import SkewnessAgregate

from scipy.stats import t


class SkewnessFederate:
    @staticmethod
    def skewness_ind(
        sample_0: LocalFederatedDataframe,
    ) -> Tuple[float]:
        if 1 != len(sample_0.columns):
            raise ValueError("sample_0 must have exactly 1 comlumn")

        list_list_precompute = []
        list_key_dataframe = list(sample_0.dict_dataframe.keys())
        # TODO deal with posibilty sample_0 and sample_1 do net share same child frames
        for key_dataframe in list_key_dataframe:
            list_list_precompute.append(
                SkewnessPrecompute.run(sample_0.dict_dataframe[key_dataframe])
            )
        skew_value = SkewnessAgregate.run(list_list_precompute)
        return skew_value

