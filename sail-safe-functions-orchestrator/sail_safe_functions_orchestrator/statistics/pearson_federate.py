from typing import Tuple
from sail_safe_functions_orchestrator.series_federated import SeriesFederated

from sail_safe_functions.statistics.pearson_agregate import PearsonAgregate
from sail_safe_functions.statistics.pearson_precompute import PearsonPrecompute


class PearsonFederate:
    """
    Computing the final Pearson Federated

    :return: _description_
    :rtype: _type_
    """

    @staticmethod
    def pearson(
        sample_0: SeriesFederated,
        sample_1: SeriesFederated,
    ) -> Tuple[float, float]:

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
        r = PearsonAgregate.run(list_list_precompute)

        return r
