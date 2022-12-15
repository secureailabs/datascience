import requests


def histogram(session, series_1_id, bin_count):
    payload = {
        "series_1_id": series_1_id,
        "bin_count": bin_count,
    }
    result = requests.post(
        "http://" + session.ip + ":" + session.port + "/visualization/histogram/",
        params=payload,
    )
    return result.json()


def kernel_density_estimation(session, series_1_id: str, bin_size: float):
    payload = {
        "series_1_id": series_1_id,
        "bin_size": bin_size,
    }
    result = requests.post(
        "http://" + session.ip + ":" + session.port + "/visualization/kernel_density_estimation/",
        params=payload,
    )
    return result.json()