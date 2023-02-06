import requests
from fast_api_client.models import (
    BodyDataframeModelAddNewSeriesModel,
    BodyNewSeriesModelNumerical,
    BodyTabularModelAddDataframeModel,
)


def new_data_model_data_frame(operation, data_frame_name):
    return operation.new_data_model_data_frame(data_frame_name).additional_properties["data_model_id"]


def new_tabular_model(operation):
    return operation.new_tabular_model().additional_properties["data_frame_tabular_id"]


def new_series_model_numerical(operation, series_name, measurement_source_name, type_aggregator, unit):
    body = BodyNewSeriesModelNumerical(series_name, measurement_source_name, type_aggregator, unit)
    # TODO: change series to series_id
    return operation.new_series_model_numerical(body).additional_properties["series"]


def data_frame_add_series(operation, dataframe_model_id, series_name, measurement_source_name, type_agregator, unit):
    body = BodyDataframeModelAddNewSeriesModel(
        dataframe_model_id, series_name, measurement_source_name, type_agregator, unit
    )

    return operation.dataframe_model_add_new_series_model(body).additional_properties["data_model_id"]


def tabular_model_add_dataframe_model(operation, data_model_tabular_id, data_model_dataframe_id):
    body = BodyTabularModelAddDataframeModel(data_model_tabular_id, data_model_dataframe_id)
    return operation.tabular_model_add_dataframe_model(body).additional_properties["data_frame_tabular_id"]
