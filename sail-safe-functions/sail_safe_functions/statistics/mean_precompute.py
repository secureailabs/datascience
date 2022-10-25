from typing import List, Tuple

import numpy as np
import pandas as pd
from sail_safe_functions_orchestrator.reference_series import ReferenceSeries
from sail_safe_functions_orchestrator.service_reference import ServiceReference


class MeanPrecompute:
    """
    Precomputes data for computing the mean
    """

    def run(
        reference_sample_0: ReferenceSeries,
    ) -> Tuple[List[float], List[bool]]:  # there seems to be a problem here with this annotation
        sample_0 = ServiceReference.get_instance().reference_to_series(reference_sample_0)
        sample_0 = sample_0.to_numpy()

        sum_x_0 = np.sum(sample_0)
        sample_0_degrees_of_freedom = len(sample_0)

        list_precompute = [sum_x_0, sample_0_degrees_of_freedom]
        # list_safe = [False, False, False, False, False, False ]
        return list_precompute  # , list_safe
