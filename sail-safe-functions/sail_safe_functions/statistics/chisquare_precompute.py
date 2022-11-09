from typing import Dict

from sail_safe_functions_orchestrator.reference_series import ReferenceSeries
from sail_safe_functions_orchestrator.service_reference import ServiceReference

from sail_safe_functions_orchestrator.tools_common import (
    check_instance,
    check_series_nan,
    check_empty_series,
    check_series_one_value,
)


class ChisquarePrecompute:
    """
    Precomputes data for Chisquare test
    """

    def run(sample_0_series: ReferenceSeries, sample_1_series: ReferenceSeries) -> Dict:
        precompute = {}

        sample_0 = ServiceReference.get_instance().reference_to_series(sample_0_series).to_numpy()
        sample_1 = ServiceReference.get_instance().reference_to_series(sample_1_series).to_numpy()
        check_empty_series(sample_0)
        check_empty_series(sample_1)
        check_series_nan(sample_0)
        check_series_nan(sample_1)
        check_series_one_value(sample_0)
        check_series_one_value(sample_1)
        for tuple_value in zip(sample_0, sample_1):
            if tuple_value not in precompute:
                precompute[tuple_value] = 0
            precompute[tuple_value] = precompute[tuple_value] + 1

        return precompute
