from ast import literal_eval

import requests


def interpret_result(result):
    if result.status_code == 200:
        return result.json()
    elif result.status_code == 500:
        return literal_eval(result.content.decode('utf-8'))['detail']
    else:
        print("Unknown Response '" + result.status_code + "': Returning Full Response Object")
        return result


def count(session, series_id):
    payload = {"series_id": series_id}
    result = requests.post(
        "https://" + session.ip + ":" + session.port + "/statistics/count/" + series_id, params=payload, verify=False
    )
    return interpret_result(result)


def mean(session, series_id):
    payload = {"series_id": series_id}
    result = requests.post(
        "https://" + session.ip + ":" + session.port + "/statistics/mean/" + series_id, params=payload, verify=False
    )
    return interpret_result(result)


def chisquare(session, series_1_id, series_2_id):
    payload = {"series_1_id": series_1_id, "series_2_id": series_2_id}
    result = requests.post(
        "https://" + session.ip + ":" + session.port + "/statistics/chisquare/" + series_1_id + "/" + series_2_id,
        params=payload,
        verify=False,
    )
    return interpret_result(result)


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
    return interpret_result(result)


def kurtosis(session, series_id):
    payload = {"series_id": series_id}
    result = requests.post(
        "https://" + session.ip + ":" + session.port + "/statistics/kurtosis/" + series_id, params=payload, verify=False
    )
    return interpret_result(result)


def levene_test(session, series_1_id, series_2_id):
    payload = {"series_1_id": series_1_id, "series_2_id": series_2_id}
    result = requests.post(
        "https://" + session.ip + ":" + session.port + "/statistics/levene_test/" + series_1_id + "/" + series_2_id,
        params=payload,
        verify=False,
    )
    return interpret_result(result)


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
    return interpret_result(result)


def min_max(session, series_1_id):
    payload = {"series_id": series_1_id}
    result = requests.post(
        "https://" + session.ip + ":" + session.port + "/statistics/min_max/" + series_1_id,
        params=payload,
        verify=False,
    )
    return interpret_result(result)


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
    return interpret_result(result)


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
    return interpret_result(result)


def skewness(session, series_id):
    payload = {"series_id": series_id}
    result = requests.post(
        "https://" + session.ip + ":" + session.port + "/statistics/skewness/" + series_id, params=payload, verify=False
    )
    return interpret_result(result)


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
    return interpret_result(result)


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
    return interpret_result(result)


def variance(session, series_id):
    payload = {"series_id": series_id}
    result = requests.post(
        "https://" + session.ip + ":" + session.port + "/statistics/variance/" + series_id, params=payload, verify=False
    )
    return interpret_result(result)


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
    return interpret_result(result)


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
    return interpret_result(result)
