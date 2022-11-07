import pandas
from sail_safe_functions_orchestrator.data_model.data_model_series import (
    DataModelSeries,
)
from sail_safe_functions_orchestrator.reference_series import ReferenceSeries
from sail_safe_functions_orchestrator.series import Series
from sail_safe_functions_orchestrator.service_reference import ServiceReference


class ConcatenatePrecompute:
    """
    Wrapper safe function for the pandas concatenate
    """

    def run(
        series_0_reference: ReferenceSeries,
        series_1_reference: ReferenceSeries,
        data_model_series: DataModelSeries,
    ) -> ReferenceSeries:
        """
        Wrapper function to conncatenate two pandas series.

            :param series_0_reference: Reference to first input series
            :type series_0_reference: ReferenceSeries
            :param series_1_reference: Reference to second input series
            :type series_1_reference: ReferenceSeries
            :param data_model_series: Data model of the series in question
            :type data_model_series: DataModelSeries
            :return: after concatenating all Series along the index (axis=0), a reference to the new series is returned.
            :rtype: ReferenceSeries
        """

        series_0 = ServiceReference.get_instance().reference_to_series(
            series_0_reference
        )
        series_1 = ServiceReference.get_instance().reference_to_series(
            series_1_reference
        )
        series_concatinated = Series(
            series_0.dataset_id,
            data_model_series,
            pandas.concat([series_0, series_1]).to_list(),
        )
        return ServiceReference.get_instance().series_to_reference(series_concatinated)
