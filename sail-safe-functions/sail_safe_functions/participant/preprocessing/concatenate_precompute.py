import pandas
from sail_safe_functions.aggregator.data_model.data_model_series import DataModelSeries
from sail_safe_functions.aggregator.reference_series import ReferenceSeries
from sail_safe_functions.aggregator.series import Series
from sail_safe_functions.aggregator.service_reference import ServiceReference
from sail_safe_functions.safe_function_base import SafeFunctionBase


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
