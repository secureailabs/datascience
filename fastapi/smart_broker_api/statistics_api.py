import requests


def count(session, series_id):
    payload = {"series_id": series_id}
    result = requests.post(
        "https://" + session.ip + ":" + session.port + "/statistics/count/" + series_id, params=payload, verify=False
    )
    return result.json()["count"]


def mean(session, series_id):
    payload = {"series_id": series_id}
    result = requests.post(
        "https://" + session.ip + ":" + session.port + "/statistics/mean/" + series_id, params=payload, verify=False
    )
    return result.json()["mean"]


def chisquare(session, series_1_id, series_2_id):
    payload = {"series_1_id": series_1_id, "series_2_id": series_2_id}
    result = requests.post(
        "https://" + session.ip + ":" + session.port + "/statistics/chisquare/" + series_1_id + "/" + series_2_id,
        params=payload,
        verify=False,
    )
    return result.json()["chisquare"]


def kolmogorovSmirnovTest(session, series_1_id, type_distribution, type_ranking):
    payload = {
        "series_1_id": series_1_id,
        "type_distribution": type_distribution,
        "type_ranking": type_ranking,
    }
    result = requests.post(
        "https://" + session.ip + ":" + session.port + "/statistics/kolmogorovSmirnovTest/" + series_1_id,
        params=payload,
        verify=False,
    )
    return result.json()["kolmogorov_smirnov_test"]


def kurtosis(session, series_id):
    payload = {"series_id": series_id}
    result = requests.post(
        "https://" + session.ip + ":" + session.port + "/statistics/kurtosis/" + series_id, params=payload, verify=False
    )
    return result.json()["kurtosis"]


def levene_test(session, series_1_id, series_2_id):
    payload = {"series_1_id": series_1_id, "series_2_id": series_2_id}
    result = requests.post(
        "https://" + session.ip + ":" + session.port + "/statistics/levene_test/" + series_1_id + "/" + series_2_id,
        params=payload,
        verify=False,
    )
    return result.json()["f_statistic_sail"], result.json()["p_value_sail"]


def mann_whitney_u_test(session, series_1_id, series_2_id, alternative, type_ranking):
    payload = {
        "series_1_id": series_1_id,
        "series_2_id": series_2_id,
        "alternative": alternative,
        "type_ranking": type_ranking,
    }
    result = requests.post(
        "https://"
        + session.ip
        + ":"
        + session.port
        + "/statistics/mann_whitney_u_test/"
        + series_1_id
        + "/"
        + series_2_id,
        params=payload,
        verify=False,
    )
    return result.json()["w_statistic_sail"], result.json()["p_value_sail"]


def min_max(session, series_1_id):
    payload = {"series_id": series_1_id}
    result = requests.post(
        "https://" + session.ip + ":" + session.port + "/statistics/min_max/" + series_1_id,
        params=payload,
        verify=False,
    )
    return result.json()["min_sail"], result.json()["max_sail"]


def paired_t_test(session, series_1_id, series_2_id, alternative):
    payload = {
        "series_1_id": series_1_id,
        "series_2_id": series_2_id,
        "alternative": alternative,
    }
    result = requests.post(
        "https://" + session.ip + ":" + session.port + "/statistics/paired_t_test/" + series_1_id + "/" + series_2_id,
        params=payload,
        verify=False,
    )
    return result.json()["t_statistic_sail"], result.json()["p_value_sail"]


def pearson(session, series_1_id, series_2_id, alternative):
    payload = {
        "series_1_id": series_1_id,
        "series_2_id": series_2_id,
        "alternative": alternative,
    }
    result = requests.post(
        "https://" + session.ip + ":" + session.port + "/statistics/pearson/" + series_1_id + "/" + series_2_id,
        params=payload,
        verify=False,
    )
    return result.json()["pearson_sail"], result.json()["p_value_sail"]


def skewness(session, series_id):
    payload = {"series_id": series_id}
    result = requests.post(
        "https://" + session.ip + ":" + session.port + "/statistics/skewness/" + series_id, params=payload, verify=False
    )
    return result.json()["skewness_sail"]


def spearman(session, series_1_id, series_2_id, alternative, type_ranking):
    payload = {
        "series_1_id": series_1_id,
        "series_2_id": series_2_id,
        "alternative": alternative,
        "type_ranking": type_ranking,
    }
    result = requests.post(
        "https://" + session.ip + ":" + session.port + "/statistics/spearman/" + series_1_id + "/" + series_2_id,
        params=payload,
        verify=False,
    )
    return result.json()["spearman_sail"], result.json()["p_value_sail"]


def student_t_test(session, series_1_id, series_2_id, alternative):
    payload = {
        "series_1_id": series_1_id,
        "series_2_id": series_2_id,
        "alternative": alternative,
    }
    result = requests.post(
        "https://" + session.ip + ":" + session.port + "/statistics/student_t_test/" + series_1_id + "/" + series_2_id,
        params=payload,
        verify=False,
    )
    return result.json()["t_statistic_sail"], result.json()["p_value_sail"]


def variance(session, series_id):
    payload = {"series_id": series_id}
    result = requests.post(
        "https://" + session.ip + ":" + session.port + "/statistics/variance/" + series_id, params=payload, verify=False
    )
    return result.json()["variance_sail"]


def welch_t_test(session, series_1_id, series_2_id, alternative):
    payload = {
        "series_1_id": series_1_id,
        "series_2_id": series_2_id,
        "alternative": alternative,
    }
    result = requests.post(
        "https://" + session.ip + ":" + session.port + "/statistics/welch_t_test/" + series_1_id + "/" + series_2_id,
        params=payload,
        verify=False,
    )
    return result.json()["t_statistic_sail"], result.json()["p_value_sail"]


def wilcoxon_signed_rank_test(session, series_1_id, series_2_id, alternative, type_ranking):
    payload = {
        "series_1_id": series_1_id,
        "series_2_id": series_2_id,
        "alternative": alternative,
        "type_ranking": type_ranking,
    }
    result = requests.post(
        "https://"
        + session.ip
        + ":"
        + session.port
        + "/statistics/wilcoxon_signed_rank_test/"
        + series_1_id
        + "/"
        + series_2_id,
        params=payload,
        verify=False,
    )
    return result.json()["w_statistic_sail"], result.json()["p_value_sail"]
