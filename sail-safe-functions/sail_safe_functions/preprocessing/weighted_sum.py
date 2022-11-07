from typing import List

import pandas
from sail_safe_functions_orchestrator.data_model.data_model_series import (
    DataModelSeries,
)
from sail_safe_functions_orchestrator.reference_series import ReferenceSeries
from sail_safe_functions_orchestrator.series import Series
from sail_safe_functions_orchestrator.service_reference import ServiceReference


class SumWeighted:
    """
    Takes the weighted sum of a list of series
    """

    def run(
        list_reference_series: List[ReferenceSeries], list_weight: List[float]
    ) -> ReferenceSeries:
        """Takes the weighted sum of a list of series

        :param list_series:list of series to be weighted
        :type list_series: List[pandas.Series]
        :param list_weight list of weights
        :type list_weight: List[float]
        :raises ValueError: raises a value exception if `list_series` and `list_weight` are not of equal lenght
        :return: returns a new series that is a weighted sum
        :rtype: pandas.Series
        """
        if len(list_reference_series) != len(list_weight):
            raise ValueError("`list_series` and `list_weight` must be of same lenght")
        series_sum = (
            ServiceReference.get_instance().reference_to_series(
                list_reference_series[0]
            )
            * 0
        )
        for reference_series, weight in zip(list_reference_series, list_weight):
            series = ServiceReference.get_instance().reference_to_series(
                reference_series
            )
            dataset_id = series.dataset_id
            series_sum += series * weight
        data_model_series = DataModelSeries.create_numerical(
            "weigthed_sum", -1, type_agregator=DataModelSeries.AgregatorComputed
        )
        series_sum = Series(dataset_id, data_model_series, series_sum.tolist())
        return ServiceReference.get_instance().series_to_reference(series_sum)
