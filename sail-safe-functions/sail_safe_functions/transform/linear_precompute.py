from array import array
from typing import List

import numpy
import pandas
from sail_safe_functions_orchestrator.data_frame import DataFrame
from sail_safe_functions_orchestrator.data_model.data_model_series import DataModelSeries
from sail_safe_functions_orchestrator.reference_data_frame import ReferenceDataFrame
from sail_safe_functions_orchestrator.series import Series
from sail_safe_functions_orchestrator.service_reference import ServiceReference


class LinearPrecompute:
    """
    Do a linear transform
    """

    def run(
        data_frame_source: ReferenceDataFrame,
        array_input: numpy.ndarray,
        list_name_series_source: List[str],
        list_name_series_target: List[str],
        inverse: bool,
    ):
        """
        Calculate precompute for Linear Transform

        :param data_frame_source: Dataframe
        :type data_frame_source: ReferenceDataFrame
        :param array: contains two things 1. array_add and 2. array_dot product
        :type array: numpy.ndarray
        :param list_name_feature_source: feature you want to do linear transform
        :type list_name_feature_source: List[str]
        :param list_name_feature_target: new feature name after transformation
        :type list_name_feature_target: List[str]
        :param inverse: To do inverse linear transform
        :type inverse: bool
        :return: dataframe
        :rtype: dataframe
        """
        data_frame_source = ServiceReference.get_instance().reference_to_data_frame(data_frame_source)

        if inverse:
            array_input = numpy.linalg.inv(array_input)

        array_source = data_frame_source[list_name_series_source].to_numpy().astype(numpy.float64)
        array_source = numpy.c_[array_source, numpy.ones(array_source.shape[0])]
        array_target = numpy.dot(array_source, array_input)

        list_series = []

        for series_name in data_frame_source.list_series_name:
            list_series.append(data_frame_source[series_name])

        for i, series_name in enumerate(list_name_series_target):
            data_model_series = DataModelSeries.create_numerical(series_name=series_name)
            series = Series(
                data_frame_source.dataset_id,
                data_model_series,
                array_target[:, i],
            )
            series.index = data_frame_source.index
            list_series.append(series)

        data_frame_target = DataFrame(data_frame_source.dataset_id, data_frame_source.data_frame_name, list_series)
        reference_data_frame_target = ServiceReference.get_instance().data_frame_to_reference(data_frame_target)
        return reference_data_frame_target
