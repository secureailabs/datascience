import requests
from fast_api_client.models import BodyDataFrameQuery


def dataframe_drop_missing(operation, data_frame_id):

    return operation.dataframe_drop_missing(data_frame_id).additional_properties["new_data_frame_id"]


def data_frame_query(operation, data_frame_id, query):

    body = BodyDataFrameQuery(data_frame_id, query)

    return operation.data_frame_query(body).additional_properties["result_data_frame_id"]


# NOTE: Doesn't work but we should allow it
# def drop_na_series(session, series_id):
#     payload = {"series_id": series_id}
#     result = requests.post(
#         "http://"
#         + session.ip
#         + ":"
#         + session.port
#         + "/preprocessing/series/drop_missing/"
#         + series_id,
#         params=payload,
#     )
#     return result.json()["series_id"]
