import requests


def count(series_id):
    payload = {"series_id": series_id}
    result = requests.post(
        "http://127.0.0.1:8000/statistics/count/" + series_id, params=payload
    )
    return result.json()["count"]


def mean(series_id):
    payload = {"series_id": series_id}
    result = requests.post(
        "http://127.0.0.1:8000/statistics/mean/" + series_id, params=payload
    )
    return result.json()["mean"]


def chisquare(series_1_id, series_2_id):
    payload = {"series_1_id": series_1_id, "series_2_id": series_2_id}
    result = requests.post(
        "http://127.0.0.1:8000/statistics/chisquare/" + series_1_id + "/" + series_2_id,
        params=payload,
    )
    return result.json()["chisquare"]


def kolmogorovSmirnovTest(series_1_id, type_distribution, type_ranking):
    payload = {
        "series_1_id": series_1_id,
        "type_distribution": type_distribution,
        "type_ranking": type_ranking,
    }
    result = requests.post(
        "http://127.0.0.1:8000/statistics/kolmogorovSmirnovTest/" + series_1_id,
        params=payload,
    )
    return result.json()["kolmogorov_smirnov_test"]


def kurtosis(series_id):
    payload = {"series_id": series_id}
    result = requests.post(
        "http://127.0.0.1:8000/statistics/kurtosis/" + series_id, params=payload
    )
    return result.json()["kurtosis"]


def levene_test(series_1_id, series_2_id):
    payload = {"series_1_id": series_1_id, "series_2_id": series_2_id}
    result = requests.post(
        "http://127.0.0.1:8000/statistics/levene_test/"
        + series_1_id
        + "/"
        + series_2_id,
        params=payload,
    )
    return result.json()["f_statistic_sail"], result.json()["p_value_sail"]


def mann_whitney_u_test(series_1_id, series_2_id, alternative, type_ranking):
    payload = {
        "series_1_id": series_1_id,
        "series_2_id": series_2_id,
        "alternative": alternative,
        "type_ranking": type_ranking,
    }
    result = requests.post(
        "http://127.0.0.1:8000/statistics/mann_whitney_u_test/"
        + series_1_id
        + "/"
        + series_2_id,
        params=payload,
    )
    return result.json()["w_statistic_sail"], result.json()["p_value_sail"]


def min_max(series_1_id):
    payload = {"series_id": series_1_id}
    result = requests.post(
        "http://127.0.0.1:8000/statistics/min_max/" + series_1_id, params=payload
    )
    return result.json()["min_sail"], result.json()["max_sail"]


def paired_t_test(series_1_id, series_2_id, alternative):
    payload = {
        "series_1_id": series_1_id,
        "series_2_id": series_2_id,
        "alternative": alternative,
    }
    result = requests.post(
        "http://127.0.0.1:8000/statistics/paired_t_test/"
        + series_1_id
        + "/"
        + series_2_id,
        params=payload,
    )
    return result.json()["t_statistic_sail"], result.json()["p_value_sail"]


def pearson(series_1_id, series_2_id, alternative):
    payload = {
        "series_1_id": series_1_id,
        "series_2_id": series_2_id,
        "alternative": alternative,
    }
    result = requests.post(
        "http://127.0.0.1:8000/statistics/pearson/" + series_1_id + "/" + series_2_id,
        params=payload,
    )
    return result.json()["pearson_sail"], result.json()["p_value_sail"]


def skewness(series_id):
    payload = {"series_id": series_id}
    result = requests.post(
        "http://127.0.0.1:8000/statistics/skewness/" + series_id, params=payload
    )
    return result.json()["skewness_sail"]


def spearman(series_1_id, series_2_id, alternative, type_ranking):
    payload = {
        "series_1_id": series_1_id,
        "series_2_id": series_2_id,
        "alternative": alternative,
        "type_ranking": type_ranking,
    }
    result = requests.post(
        "http://127.0.0.1:8000/statistics/spearman/" + series_1_id + "/" + series_2_id,
        params=payload,
    )
    return result.json()["spearman_sail"], result.json()["p_value_sail"]


def student_t_test(series_1_id, series_2_id, alternative):
    payload = {
        "series_1_id": series_1_id,
        "series_2_id": series_2_id,
        "alternative": alternative,
    }
    result = requests.post(
        "http://127.0.0.1:8000/statistics/student_t_test/"
        + series_1_id
        + "/"
        + series_2_id,
        params=payload,
    )
    return result.json()["t_statistic_sail"], result.json()["p_value_sail"]


def variance(series_id):
    payload = {"series_id": series_id}
    result = requests.post(
        "http://127.0.0.1:8000/statistics/variance/" + series_id, params=payload
    )
    return result.json()["variance_sail"]


def welch_t_test(series_1_id, series_2_id, alternative):
    payload = {
        "series_1_id": series_1_id,
        "series_2_id": series_2_id,
        "alternative": alternative,
    }
    result = requests.post(
        "http://127.0.0.1:8000/statistics/welch_t_test/"
        + series_1_id
        + "/"
        + series_2_id,
        params=payload,
    )
    return result.json()["t_statistic_sail"], result.json()["p_value_sail"]


def wilcoxon_signed_rank_test(series_1_id, series_2_id, alternative, type_ranking):
    payload = {
        "series_1_id": series_1_id,
        "series_2_id": series_2_id,
        "alternative": alternative,
        "type_ranking": type_ranking,
    }
    result = requests.post(
        "http://127.0.0.1:8000/statistics/wilcoxon_signed_rank_test/"
        + series_1_id
        + "/"
        + series_2_id,
        params=payload,
    )
    return result.json()["w_statistic_sail"], result.json()["p_value_sail"]
