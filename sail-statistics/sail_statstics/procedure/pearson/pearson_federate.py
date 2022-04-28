from typing import Tuple
from sail_statstics.local_federated_dataframe import LocalFederatedDataframe

from sail_statstics.procedure.pearson.pearson_precompute import PearsonPrecompute
from sail_statstics.procedure.pearson.pearson_agregate import PearsonAgregate


class PearsonFederate:
    @staticmethod
    def pearson(
        sample_0: LocalFederatedDataframe,
        sample_1: LocalFederatedDataframe,
    ) -> Tuple[float, float]:

        list_list_precompute = []
        print(list_list_precompute)
        list_key_dataframe = list(sample_0.dict_dataframe.keys())
        # TODO deal with posibilty sample_0 and sample_1 do net share same child frames
        for key_dataframe in list_key_dataframe:
            list_list_precompute.append(
                PearsonPrecompute.run(sample_0.dict_dataframe[key_dataframe], sample_1.dict_dataframe[key_dataframe])
            )

        r = PearsonAgregate.run(list_list_precompute)

        return r
