from typing import List, Tuple

import numpy as np
import pandas as pd
from sail_safe_functions_orchestrator.reference_series import ReferenceSeries
from sail_safe_functions_orchestrator.service_reference import ServiceReference
from sail_safe_functions_orchestrator.tools_common import (
    check_instance,
    check_series_nan,
    check_empty_series,
    check_series_one_value,
)


class CountPrecompute:
    """
    Precomputes data for computing the count
    """

    def run(
        sample_0_series: ReferenceSeries,
    ) -> float:
        sample_0 = ServiceReference.get_instance().reference_to_series(sample_0_series).to_numpy()
        check_empty_series(sample_0)
        return sample_0.size
