from typing import Tuple

import numpy
import pandas
from sail_safe_functions_orchestrator.reference_series import ReferenceSeries
from sail_safe_functions_orchestrator.service_reference import ServiceReference


class WilcoxonSingedRankTestPrecompute:
    """
    Precomputes data for the  WilcoxonSingedRankTest
    """

    def run(
        reference_sample_difference: ReferenceSeries,
        reference_sample_absolute_difference_ranked: ReferenceSeries,
    ) -> Tuple[float, float]:
        sample_difference = ServiceReference.get_instance().reference_to_series(reference_sample_difference).to_numpy()
        sample_absolute_difference_ranked = (
            ServiceReference.get_instance().reference_to_series(reference_sample_absolute_difference_ranked).to_numpy()
        )

        rank_minus = numpy.sum((sample_difference < 0) * sample_absolute_difference_ranked)
        rank_plus = numpy.sum((sample_difference > 0) * sample_absolute_difference_ranked)
        return [rank_minus, rank_plus]
