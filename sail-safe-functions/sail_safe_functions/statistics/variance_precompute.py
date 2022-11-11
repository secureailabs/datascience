from typing import List, Tuple

import numpy as np
import pandas as pd
from sail_safe_functions_orchestrator.reference_series import ReferenceSeries
from sail_safe_functions_orchestrator.service_reference import ServiceReference


class VariancePrecompute:
    """
    Precomputes data for computing the variance
    """

    def run(
        sample_0_series: ReferenceSeries,
    ) -> Tuple[List[float], List[bool]]:  # there seems to be a problem here with this annotation
        sample_0 = ServiceReference.get_instance().reference_to_series(sample_0_series).to_numpy()
        sum_x_0 = np.sum(sample_0)
        sum_xx_0 = np.sum(sample_0 * sample_0)
        sample_0_dof = len(sample_0)

        list_precompute = [sum_x_0, sum_xx_0, sample_0_dof]
        return list_precompute
