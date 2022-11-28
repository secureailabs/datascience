import requests


def create_date_frame(data_frame_name):
    payload = {"data_frame_name": data_frame_name}
    result = requests.post(
        "http://127.0.0.1:8000/data_model/new_data_frame_model", params=payload
    )
    return result.json()["data_model_id"]


def create_tabular_data():
    result = requests.post(
        "http://127.0.0.1:8000/data_model/new_tabular_model", params=None
    )
    return result.json()["data_frame_tabular_id"]


def data_frame_add_series(data_model_id, series_name, measurement_source_name):
    payload = {
        "data_model_id": data_model_id,
        "series_name": series_name,
        "measurement_source_name": measurement_source_name,
    }
    result = requests.post(
        "http://127.0.0.1:8000/data_model/data_frame/"
        + data_model_id
        + "/add_new_series_model",
        params=payload,
    )
    return result.json()["data_model_id"]


def tabular_add_dataframe(data_model_dataframe_id, data_model_tabular_id):
    payload = {
        "data_model_dataframe_id": data_model_dataframe_id,
        "data_model_tabular_id": data_model_tabular_id,
    }
    result = requests.post(
        "http://127.0.0.1:8000/data_model/tabular/"
        + data_model_tabular_id
        + "/add_dataframe",
        params=payload,
    )
    return result.json()["data_frame_tabular_id"]
