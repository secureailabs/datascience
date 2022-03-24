from sail_statstics.local_federated_dataframe import LocalFederatedDataframe

from sail_statstics.procedure.mean.mean_precompute import MeanPrecompute
from sail_statstics.procedure.mean.mean_agregate import MeanAgregate


class MeanFederate:
    @staticmethod
    def mean(sample_0: LocalFederatedDataframe):

        list_list_precompute = []
        list_key_dataframe = list(sample_0.dict_dataframe.keys())
        # TODO deal with posibilty sample_0 and sample_1 do net share same child frames
        # TODO deal with posibilty sample_0 and sample_1 have more than 1 column
        for key_dataframe in list_key_dataframe:
            list_list_precompute.append(MeanPrecompute.run(sample_0.dict_dataframe[key_dataframe]))

        mean_statistic = MeanAgregate.run(list_list_precompute)

        return mean_statistic
