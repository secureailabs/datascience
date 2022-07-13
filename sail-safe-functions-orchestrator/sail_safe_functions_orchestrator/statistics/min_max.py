from typing import Tuple

import numpy
from sail_safe_functions.statistics.min_max_agregate import MinMaxAgregate
from sail_safe_functions.statistics.min_max_precompute import MinMaxPrecompute
from sail_safe_functions_orchestrator.series_federated import SeriesFederated
from sail_safe_functions_orchestrator.statistics.estimator import Estimator


def min_max(sample_0: SeriesFederated) -> Tuple[float, float]:
    estimator = MinMax()
    return estimator.run(sample_0)


class MinMax(Estimator):
    """
    Class that wraps the safe function for min and max
    """

    def __init__(self) -> None:
        super().__init__(["min", "max"])

    def run(self, sample_0: SeriesFederated) -> Tuple[float, float]:
        list_list_precompute = []
        # TODO deal with posibilty sample_0 and sample_1 do not share same child frames

        # Calculating precompute
        for series in sample_0.dict_series.values():  # TODO replace these
            list_list_precompute.append(MinMaxPrecompute.run(series))

        # Final min max values
        min, max = MinMaxAgregate.run(list_list_precompute)
        return min, max

    def run_reference(self, sample_0: SeriesFederated) -> Tuple[float, float]:
        min_numpy = numpy.min(sample_0.to_numpy())  # TODO this is ugly as fuck
        max_numpy = numpy.max(sample_0.to_numpy())
        return min_numpy, max_numpy