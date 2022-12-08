from typing import List

from sail_safe_functions.safe_function_base import SafeFunctionBase
from sail_safe_functions_orchestrator.reference_series import ReferenceSeries
from sail_safe_functions_orchestrator.service_reference import ServiceReference


class KernelDensityEstimationPrecompute(SafeFunctionBase):
    """
    Precomputes data for kernel density estimation
    """

    @staticmethod
    def run(sample_0_series: ReferenceSeries) -> List[float]:
        """Generates the precompute count Frequency

        Parameters
        ----------
        sample_0_series : pd.series
            The series for sample_0
        Returns
        -------
        return two list :
        list_1 : Unique values in the series
        list_2 : list of frequecy(count of total number of time each vallue came in the seires) of every unique value.
        """
        # series containing unique value in index and frequency.
        sample_0 = ServiceReference.get_instance().reference_to_series(sample_0_series)
        series = sample_0.value_counts()
        l1 = list(series.index)
        l2 = list(series)

        list_precompute = [l1, l2]

        return list_precompute
