import numpy
import pandas
from sail_safe_functions.preprocessing.convert.categorical_to_onehot import CategoricalToOnehot
from sail_safe_functions.safe_function_base import SafeFunctionBase
from sail_safe_functions_orchestrator.data_frame import DataFrame
from sail_safe_functions_orchestrator.data_model.data_model_series import DataModelSeries
from sail_safe_functions_orchestrator.reference_data_frame import ReferenceDataFrame
from sail_safe_functions_orchestrator.series import Series
from sail_safe_functions_orchestrator.service_reference import ServiceReference


class TabularToFloat64Precompute(SafeFunctionBase):
    def run(reference_data_frame_source: ReferenceDataFrame) -> ReferenceDataFrame:

        data_frame_source = ServiceReference.get_instance().reference_to_data_frame(reference_data_frame_source)
        list_series = []
        for series_name in data_frame_source.list_series_name:
            series_source = data_frame_source[series_name]

            if series_source.data_model_series.type_data_level == DataModelSeries.DataLevelUnique:
                pass
            elif series_source.data_model_series.type_data_level == DataModelSeries.DataLevelCategorical:
                list_series.extend(CategoricalToOnehot.run(series_source))

            elif series_source.data_model_series.type_data_level == DataModelSeries.DataLevelInterval:
                series_pandas = series_source.astype(numpy.float64)
                series = Series.from_pandas(
                    data_frame_source.dataset_id, data_frame_source.data_model_data_frame[series_name], series_pandas
                )
                series.index = series_pandas.index
                list_series.append(series)

        data_frame_target = DataFrame(data_frame_source.dataset_id, data_frame_source.data_frame_name, list_series)
        reference_data_frame_target = ServiceReference.get_instance().data_frame_to_reference(data_frame_target)
        return reference_data_frame_target
