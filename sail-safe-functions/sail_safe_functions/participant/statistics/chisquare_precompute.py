from typing import Dict

from sail_core.tools_common import sanitize_dict_for_json
from sail_safe_functions.aggregator.reference_series import ReferenceSeries
from sail_safe_functions.aggregator.service_reference import ServiceReference
from sail_safe_functions.aggregator.tools_common import check_empty_series, check_series_nan, check_series_one_value
from sail_safe_functions.safe_function_base import SafeFunctionBase


class ChisquarePrecompute(SafeFunctionBase):
    """
    Precomputes data for Chisquare test
    """

    @staticmethod
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

        for val_0, val_1 in zip(sample_0, sample_1):
            tuple_value = val_0 + "___" + val_1  # TODO this magic value stuf is BS
            if tuple_value not in precompute:
                precompute[tuple_value] = 0
            precompute[tuple_value] = precompute[tuple_value] + 1

        precompute = sanitize_dict_for_json(precompute)
        return precompute
