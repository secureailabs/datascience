from sail_safe_functions.safe_function_base import SafeFunctionBase
from sail_safe_functions_orchestrator.data_model.data_model_series import DataModelSeries
from sail_safe_functions_orchestrator.reference_series import ReferenceSeries
from sail_safe_functions_orchestrator.series import Series
from sail_safe_functions_orchestrator.service_reference import ServiceReference


# TODO this function is dangerous
class ValueAbsolute(SafeFunctionBase):
    """
    Takes the absolute value sum of a series
    """

    @staticmethod
    def run(reference_series_0: ReferenceSeries) -> ReferenceSeries:
        """
        Takes the weighted sum of a list of series and outputs absolute value of the series

        :param series_0: input series
        :type series_0: ReferenceSeries
        :return: returns a new series that is a absolute value
        :rtype: ReferenceSeries
        """
        series_0 = ServiceReference.get_instance().reference_to_series(reference_series_0)

        data_model_series = DataModelSeries.create_numerical(
            "absolute", -1, type_agregator=DataModelSeries.AgregatorComputed
        )
        series_sum = Series(reference_series_0.dataset_id, data_model_series, series_0.abs().tolist())
        return ServiceReference.get_instance().series_to_reference(series_sum)
