from ast import literal_eval

import requests
from fast_api_client.models import (
    BodyMannWhitneyUTest,
    BodyStatisticsChisquare,
    BodyStatisticsKolmogorovSmirnovTest,
    BodyStatisticsLeveneTest,
    BodyStatisticsPairedTTest,
    BodyStatisticsPearson,
    BodyStatisticsSpearman,
    BodyStatisticsStudentTTest,
    BodyStatisticsWelchTTest,
    BodyStatisticsWilcoxonSignedRankTest,
)

# def interpret_result(result):
#     if result.status_code == 200:
#         return result.json()
#     elif result.status_code == 500:
#         return literal_eval(result.content.decode("utf-8"))["detail"]
#     else:
#         print("Unknown Response '" + result.status_code + "': Returning Full Response Object")
#         return result


def count(operation, series_id):
    return operation.statistics_count(series_id).additional_properties["count"]


def mean(operation, series_id):
    return operation.statistics_mean(series_id).additional_properties["mean"]


def chisquare(operation, series_1_id, series_2_id):
    body = BodyStatisticsChisquare(series_1_id, series_2_id)
    return operation.statistics_chisquare(body).additional_properties["chisquare"]


def kolmogorov_smirnov_test(operation, series_1_id, type_distribution):

    body = BodyStatisticsKolmogorovSmirnovTest(series_1_id, type_distribution)
    return operation.statistics_kolmogorov_smirnov_test(body).additional_properties["kolmogorov_smirnov_test"]


def kurtosis(operation, series_id):
    return operation.statistics_kurtosis(series_id).additional_properties["kurtosis"]


def levene_test(operation, series_1_id, series_2_id):

    body = BodyStatisticsLeveneTest(series_1_id, series_2_id)

    result = operation.statistics_levene_test(body).additional_properties

    return result["f_statistic"], result["p_value"]


def mann_whitney_u_test(operation, series_1_id, series_2_id, alternative):
    payload = {
        "series_1_id": series_1_id,
        "series_2_id": series_2_id,
        "alternative": alternative,
    }

    body = BodyMannWhitneyUTest(series_1_id, series_2_id, alternative)
    result = operation.mann_whitney_u_test(body).additional_properties

    return result["w_statistic"], result["p_value"]


def min_max(operation, series_1_id):

    result = operation.statistics_min_max(series_1_id).additional_properties

    return result["min"], result["max"]


def paired_t_test(operation, series_1_id, series_2_id, alternative):

    body = BodyStatisticsPairedTTest(series_1_id, series_2_id, alternative)

    result = operation.statistics_paired_t_test(body).additional_properties

    return result["t_statistic"], result["p_value"]


def pearson(operation, series_1_id, series_2_id, alternative):

    body = BodyStatisticsPearson(series_1_id, series_2_id, alternative)

    result = operation.statistics_pearson(body).additional_properties

    return result["pearson"], result["p_value"]


def skewness(operation, series_id):

    return operation.statistics_skewness(series_id).additional_properties["skewness"]


def spearman(operation, series_1_id, series_2_id, alternative):

    body = BodyStatisticsSpearman(series_1_id, series_2_id, alternative)
    result = operation.statistics_spearman(body)

    return result["spearman"], result["p_value"]


def student_t_test(operation, series_1_id, series_2_id, alternative):

    body = BodyStatisticsStudentTTest(series_1_id, series_2_id, alternative)
    result = operation.statistics_student_t_test(body).additional_properties

    return result["t_statistic"], result["p_value"]


def variance(operation, series_id):
    return operation.statistics_variance(series_id).additional_properties["variance"]


def welch_t_test(operation, series_1_id, series_2_id, alternative):
    body = BodyStatisticsWelchTTest(series_1_id, series_2_id, alternative)
    result = operation.statistics_welch_t_test(body).additional_properties
    return result["t_statistic"], result["p_value"]


def wilcoxon_signed_rank_test(operation, series_1_id, series_2_id, alternative):
    body = BodyStatisticsWilcoxonSignedRankTest(series_1_id, series_2_id, alternative)
    result = operation.statistics_wilcoxon_signed_rank_test(body)
    return result["w_statistic"], result["p_value"]
