from typing import Dict

from sail_safe_functions_orchestrator.reference_series import ReferenceSeries
from sail_safe_functions_orchestrator.service_reference import ServiceReference


class ChisquarePrecompute:
    """
    Precomputes data for Chisquare test
    """

    def run(sample_0_series: ReferenceSeries, sample_1_series: ReferenceSeries) -> Dict:
        precompute = {}

        sample_0 = ServiceReference.get_instance().reference_to_series(sample_0_series).to_numpy()
        sample_1 = ServiceReference.get_instance().reference_to_series(sample_1_series).to_numpy()
        for tuple_value in zip(sample_0, sample_1):
            if tuple_value not in precompute:
                precompute[tuple_value] = 0
            precompute[tuple_value] = precompute[tuple_value] + 1

        return precompute
