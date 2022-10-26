import pandas
from sail_safe_functions_orchestrator.reference_series import ReferenceSeries
from sail_safe_functions_orchestrator.service_reference import ServiceReference


class MannWhitneyUTestPrecompute:
    """
    The precompute function of the mann withnet u test
    """

    def run(reference_series_0: ReferenceSeries, reference_series_concatenated_ranked: ReferenceSeries) -> float:
        series_0 = ServiceReference.get_instance().reference_to_series(reference_series_0).to_numpy()
        series_concatenated_ranked = (
            ServiceReference.get_instance().reference_to_series(reference_series_concatenated_ranked).to_numpy()
        )
        return series_concatenated_ranked[: series_0.size].sum()
