import pandas
from sail_safe_functions.safe_function_base import SafeFunctionBase
from sail_safe_functions_orchestrator.data_model.data_model_series import DataModelSeries
from sail_safe_functions_orchestrator.reference_series import ReferenceSeries
from sail_safe_functions_orchestrator.series import Series
from sail_safe_functions_orchestrator.service_reference import ServiceReference


class ConcatenatePrecompute(SafeFunctionBase):
    """Wrapper safe function for the pandas concatenate"""

    def run(
        series_0_reference: ReferenceSeries, series_1_reference: ReferenceSeries, data_model_series: DataModelSeries
    ) -> ReferenceSeries:

        series_0 = ServiceReference.get_instance().reference_to_series(series_0_reference)
        series_1 = ServiceReference.get_instance().reference_to_series(series_1_reference)
        series_concatinated = Series(
            series_0.dataset_id, data_model_series, pandas.concat([series_0, series_1]).to_list()
        )
        return ServiceReference.get_instance().series_to_reference(series_concatinated)
