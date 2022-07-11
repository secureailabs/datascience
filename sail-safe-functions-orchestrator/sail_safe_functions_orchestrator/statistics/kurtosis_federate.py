from typing import Tuple

import pandas
from sail_safe_functions.statistics.kurtosis_agregate import KurtosisAgregate
from sail_safe_functions.statistics.kurtosis_precompute import KurtosisPrecompute
from sail_safe_functions_orchestrator.series_federated import SeriesFederated
from sail_safe_functions_orchestrator.statistics.estimator import Estimator
from scipy import stats


class KurtosisFederate(Estimator):
    """
    Final function to run for Kurtosis Fedrated
    """

    def __init__(self) -> None:
        super().__init__()
        self.list_name_estimate = ["kurtosis"]

    @staticmethod
    def kurtosis(
        sample_0: SeriesFederated,
    ) -> Tuple[float]:
        estimator = KurtosisFederate()
        return estimator.run(sample_0)

    def run(self, sample_0: SeriesFederated):
        list_list_precompute = []
        # TODO deal with posibilty sample_0 and sample_1 do net share same child frames

        # Calculating precompute
        for series in sample_0.dict_series.values():
            list_list_precompute.append(KurtosisPrecompute.run(series))

        # Final Kurtosis Value
        kurtosis_value = KurtosisAgregate.run(list_list_precompute)
        return kurtosis_value

    def run_reference(self, sample_0: SeriesFederated):
        return stats.kurtosis(sample_0.to_numpy())
