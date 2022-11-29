import requests


def drop_na_data_frame(session, data_frame_id):
    payload = {"data_frame_id": data_frame_id}
    result = requests.post(
        "http://"
        + session.ip
        + ":"
        + session.port
        + "/preprocessing/data_frame/drop_missing/"
        + data_frame_id,
        params=payload,
    )
    return result.json()["result_data_frame_id"]


## Doesn't work but we should allou it
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
