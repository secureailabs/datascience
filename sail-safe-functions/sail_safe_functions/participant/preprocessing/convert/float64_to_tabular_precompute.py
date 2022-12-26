import pandas
from sail_safe_functions.aggregator.data_frame import DataFrame
from sail_safe_functions.aggregator.data_model.data_model_data_frame import DataModelDataFrame
from sail_safe_functions.aggregator.data_model.data_model_series import DataModelSeries
from sail_safe_functions.aggregator.reference_data_frame import ReferenceDataFrame
from sail_safe_functions.aggregator.series import Series
from sail_safe_functions.aggregator.service_reference import ServiceReference
from sail_safe_functions.participant.preprocessing.convert.onehot_to_categorical import OnehotToCategorical
from sail_safe_functions.safe_function_base import SafeFunctionBase


class Float64ToTabularPrecompute(SafeFunctionBase):
    @staticmethod
    def run(
        reference_data_frame_source: ReferenceDataFrame, data_model_target: DataModelDataFrame
    ) -> ReferenceDataFrame:
        data_frame_source = ServiceReference.get_instance().reference_to_data_frame(reference_data_frame_source)
        list_series = []
        for series_name in data_model_target.list_series_name:
            data_model_series = data_model_target[series_name]
            if data_model_series.type_data_level == DataModelSeries.DataLevelUnique:
                pass

            if data_model_series.type_data_level == DataModelSeries.DataLevelCategorical:
                list_series.append(OnehotToCategorical.run(data_frame_source, data_model_series))

            elif data_model_series.type_data_level == DataModelSeries.DataLevelInterval:
                series_pandas = data_frame_source[series_name]
                resolution = data_model_series.resolution
                if (resolution is not None) and (resolution != -1):  # TODO oldfassioned maybe avoid magic value
                    series_pandas = (series_pandas * (1 / resolution)).round().astype(int) * resolution
                series = Series.from_pandas(data_frame_source.dataset_id, data_model_series, series_pandas)
                series.index = series_pandas.index
                list_series.append(series)

        data_frame_target = DataFrame(data_frame_source.dataset_id, data_frame_source.data_frame_name, list_series)
        reference_data_frame_target = ServiceReference.get_instance().data_frame_to_reference(data_frame_target)
        return reference_data_frame_target
