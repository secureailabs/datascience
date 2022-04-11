from typing import Tuple
from sail_statstics.local_federated_dataframe import LocalFederatedDataframe

from sail_statstics.procedure.skewness.skewness_precompute import SkewnessPrecompute
from sail_statstics.procedure.skewness.skewness_agregate import SkewnessAgregate


class SkewnessFederate:

    """
    Final function to run for skewness Fedrated
    :return: Tupel[Float]
    :rtype: _type_
    """

    @staticmethod
    def skewness_ind(
        sample_0: LocalFederatedDataframe,
    ) -> Tuple[float]:

        if 1 != len(sample_0.columns):
            raise ValueError("sample_0 must have exactly 1 comlumn")

        list_list_precompute = []
        list_key_dataframe = list(sample_0.dict_dataframe.keys())
        # TODO deal with posibilty sample_0 and sample_1 do net share same child frames

        # Calculating precompute
        for key_dataframe in list_key_dataframe:
            list_list_precompute.append(SkewnessPrecompute.run(sample_0.dict_dataframe[key_dataframe]))
        # Final Skew Value
        skew_value = SkewnessAgregate.run(list_list_precompute)
        return skew_value
