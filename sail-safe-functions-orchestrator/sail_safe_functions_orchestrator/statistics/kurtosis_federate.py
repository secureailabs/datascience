from typing import Tuple

from sail_safe_functions.statistics.kurtosis_agregate import KurtosisAgregate
from sail_safe_functions.statistics.kurtosis_precompute import KurtosisPrecompute
from sail_safe_functions_orchestrator.series_federated import SeriesFederated


class KurtosisFederate:

    """
    Final function to run for Kurtosis Fedrated
    """

    @staticmethod
    def kurtosis(
        sample_0: SeriesFederated,
    ) -> Tuple[float]:

        list_list_precompute = []
        # TODO deal with posibilty sample_0 and sample_1 do net share same child frames

        # Calculating precompute
        for series in sample_0.dict_series.values():
            list_list_precompute.append(KurtosisPrecompute.run(series))

        # Final Kurtosis Value
        kurtosis_value = KurtosisAgregate.run(list_list_precompute)
        return kurtosis_value
