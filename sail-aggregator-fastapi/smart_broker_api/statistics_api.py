# from ast import literal_eval
from typing import Tuple

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
from fast_api_client.sail_class import SyncOperations

# def interpret_result(result):
#     if result.status_code == 200:
#         return result.json()
#     elif result.status_code == 500:
#         return literal_eval(result.content.decode("utf-8"))["detail"]
#     else:
#         print("Unknown Response '" + result.status_code + "': Returning Full Response Object")
#         return result


def count(operation: SyncOperations, series_1_id: str) -> int:
    """
    Performs federated count on sample series.
    Parameters
    ----------
    :param operation: Object used to reference fast_api_client function calls
    :type operation: SyncOperations
    :param series_1_id: The id of the series to be processed
    :type series_1_id: string

    Returns
    -------
    int
       The count of the sample series.
    """
    return operation.statistics_count(series_1_id).additional_properties["count"]


def mean(operation: SyncOperations, series_1_id: str):
    """
    Performs federated mean on sample series.
    Parameters
    ----------
    :param operation: Object used to reference fast_api_client function calls
    :type operation: SyncOperations
    :param series_1_id: The id of the series to be processed
    :type series_1_id: string

    Returns
    -------
    int
       The mean of the sample series.
    """
    return operation.statistics_mean(series_1_id).additional_properties["mean"]


def chisquare(operation: SyncOperations, series_1_id: str, series_2_id: str) -> Tuple[float, float]:
    """
    Calculates federated chisquare of two sample series.
    Parameters
    ----------
    :param operation: Object used to reference fast_api_client function calls
    :type operation: SyncOperations
    :param series_1_id: The id of the series to be processed
    :type series_1_id: string
    :param series_2_id: The id of the series to be processed
    :type series_2_id: string

    Returns
    -------
    float
       The chisquare statistic of the sample series.
    float
       The p-value of the sample series.
    """
    body = BodyStatisticsChisquare(series_1_id, series_2_id)
    return operation.statistics_chisquare(body).additional_properties["chisquare"]


def kolmogorov_smirnov_test(operation: SyncOperations, series_1_id: str, type_distribution: str) -> Tuple[float, float]:
    """
    Executes a Kolmogorov Smirnov Test checking if a given series follows the given distribution.
    ----------
    :param operation: Object used to reference fast_api_client function calls
    :type operation: SyncOperations
    :param series_1_id: The id of the series to be processed
    :type series_1_id: string
    :param type_distribution: The type of distribution tp be compared against the sample, may be `normal` or `normalunit`
    :type type_distribution: string

    Returns
    -------
    float
       The K statistic of the sample series.
    float
       The p-value of the sample series compared to the distriubtion.
    """
    body = BodyStatisticsKolmogorovSmirnovTest(series_1_id, type_distribution)
    result = operation.statistics_kolmogorov_smirnov_test(body).additional_properties["kolmogorov_smirnov_test"]
    return result[0], result[1]


def kurtosis(operation: SyncOperations, series_1_id: str) -> float:
    """
    Computes federated kurtosis of sample series.
    Parameters
    ----------
    :param operation: Object used to reference fast_api_client function calls
    :type operation: SyncOperations
    :param series_1_id: The id of the series to be processed
    :type series_1_id: string

    Returns
    -------
    float
       The kurtosis of the sample series.
    """
    return operation.statistics_kurtosis(series_1_id).additional_properties["kurtosis"]


def levene_test(operation: SyncOperations, series_1_id: str, series_2_id: str) -> Tuple[float, float]:
    """
    Calculates federated levene test of two sample series.
    Parameters
    ----------
    :param operation: Object used to reference fast_api_client function calls
    :type operation: SyncOperations
    :param series_1_id: The id of the series to be processed
    :type series_1_id: string
    :param series_2_id: The id of the series to be processed
    :type series_2_id: string

    Returns
    -------
    float
       The f statistic of the sample series.
    float
       The p-value of the sample series.
    """

    body = BodyStatisticsLeveneTest(series_1_id, series_2_id)

    result = operation.statistics_levene_test(body).additional_properties

    return result["f_statistic"], result["p_value"]


def mann_whitney_u_test(
    operation: SyncOperations, series_1_id: str, series_2_id: str, alternative: str
) -> Tuple[float, float]:
    """
    Calculates Mann Whitney U Test test of two sample series.
    Parameters
    ----------
    :param operation: Object used to reference fast_api_client function calls
    :type operation: SyncOperations
    :param series_1_id: The id of the series to be processed
    :type series_1_id: string
    :param series_2_id: The id of the series to be processed
    :type series_2_id: string
    :param alternative: The alternative used. May be "less", "two-sided" or "greater"
    :type alternative: string

    Returns
    -------
    float
       The w statistic of the sample series.
    float
       The p-value of the sample series.
    """

    body = BodyMannWhitneyUTest(series_1_id, series_2_id, alternative)
    result = operation.mann_whitney_u_test(body).additional_properties

    return result["w_statistic"], result["p_value"]


def min_max(operation: SyncOperations, series_1_id: str) -> Tuple[float, float]:
    """
    Finds the mininmum and maximum values of sample federated series.
    Parameters
    ----------
    :param operation: Object used to reference fast_api_client function calls
    :type operation: SyncOperations
    :param series_1_id: The id of the series to be processed
    :type series_1_id: string

    Returns
    -------
    float
       The minimum value of the sample series.
    float
       The maximum value of the sample series.
    """

    result = operation.statistics_min_max(series_1_id).additional_properties

    return result["min"], result["max"]


def paired_t_test(
    operation: SyncOperations, series_1_id: str, series_2_id: str, alternative: str
) -> Tuple[float, float]:
    """
    Calculates paired T Test test of two sample series.
    Parameters
    ----------
    :param operation: Object used to reference fast_api_client function calls
    :type operation: SyncOperations
    :param series_1_id: The id of the series to be processed
    :type series_1_id: string
    :param series_2_id: The id of the series to be processed
    :type series_2_id: string
    :param alternative: The alternative used. May be "less", "two-sided" or "greater"
    :type alternative: string

    Returns
    -------
    float
       The t statistic of the sample series.
    float
       The p-value of the sample series.
    """
    body = BodyStatisticsPairedTTest(series_1_id, series_2_id, alternative)

    result = operation.statistics_paired_t_test(body).additional_properties

    return result["t_statistic"], result["p_value"]


def pearson(operation: SyncOperations, series_1_id: str, series_2_id: str, alternative: str) -> Tuple[float, float]:
    """
    Calculates the Pearson statistic of two sample series.
    Parameters
    ----------
    :param operation: Object used to reference fast_api_client function calls
    :type operation: SyncOperations
    :param series_1_id: The id of the series to be processed
    :type series_1_id: string
    :param series_2_id: The id of the series to be processed
    :type series_2_id: string
    :param alternative: The alternative used. May be "less", "two-sided" or "greater"
    :type alternative: string

    Returns
    -------
    float
       The pearson statistic of the sample series.
    float
       The p-value of the sample series.
    """
    body = BodyStatisticsPearson(series_1_id, series_2_id, alternative)

    result = operation.statistics_pearson(body).additional_properties

    return result["pearson"], result["p_value"]


def skewness(operation: SyncOperations, series_1_id: str) -> float:
    """
    Computes the skewness of sample federated series.
    Parameters
    ----------
    :param operation: Object used to reference fast_api_client function calls
    :type operation: SyncOperations
    :param series_1_id: The id of the series to be processed
    :type series_1_id: string

    Returns
    -------
    float
       The skewness value of the sample series.
    """

    return operation.statistics_skewness(series_1_id).additional_properties["skewness"]


def spearman(operation: SyncOperations, series_1_id: str, series_2_id: str, alternative: str) -> Tuple[float, float]:
    """
    Calculates the Spearman statistic of two sample series.
    Parameters
    ----------
    :param operation: Object used to reference fast_api_client function calls
    :type operation: SyncOperations
    :param series_1_id: The id of the series to be processed
    :type series_1_id: string
    :param series_2_id: The id of the series to be processed
    :type series_2_id: string
    :param alternative: The alternative used. May be "less", "two-sided" or "greater"
    :type alternative: string

    Returns
    -------
    float
       The spearman statistic of the sample series.
    float
       The p-value of the sample series.
    """
    body = BodyStatisticsSpearman(series_1_id, series_2_id, alternative)
    result = operation.statistics_spearman(body)

    return result["spearman"], result["p_value"]


def student_t_test(
    operation: SyncOperations, series_1_id: str, series_2_id: str, alternative: str
) -> Tuple[float, float]:
    """
    Calculates the student T test of two sample series.
    Parameters
    ----------
    :param operation: Object used to reference fast_api_client function calls
    :type operation: SyncOperations
    :param series_1_id: The id of the series to be processed
    :type series_1_id: string
    :param series_2_id: The id of the series to be processed
    :type series_2_id: string
    :param alternative: The alternative used. May be "less", "two-sided" or "greater"
    :type alternative: string

    Returns
    -------
    float
       The t statistic of the sample series.
    float
       The p-value of the sample series.
    """
    body = BodyStatisticsStudentTTest(series_1_id, series_2_id, alternative)
    result = operation.statistics_student_t_test(body).additional_properties

    return result["t_statistic"], result["p_value"]


def variance(operation: SyncOperations, series_1_id: str) -> float:
    """
    Computes the variance of sample federated series.
    Parameters
    ----------
    :param operation: Object used to reference fast_api_client function calls
    :type operation: SyncOperations
    :param series_1_id: The id of the series to be processed
    :type series_1_id: string

    Returns
    -------
    float
       The variance value of the sample series.
    """
    return operation.statistics_variance(series_1_id).additional_properties["variance"]


def welch_t_test(
    operation: SyncOperations, series_1_id: str, series_2_id: str, alternative: str
) -> Tuple[float, float]:
    """
    Calculates the Welch T test of two sample series.
    Parameters
    ----------
    :param operation: Object used to reference fast_api_client function calls
    :type operation: SyncOperations
    :param series_1_id: The id of the series to be processed
    :type series_1_id: string
    :param series_2_id: The id of the series to be processed
    :type series_2_id: string
    :param alternative: The alternative used. May be "less", "two-sided" or "greater"
    :type alternative: string

    Returns
    -------
    float
       The t statistic of the sample series.
    float
       The p-value of the sample series.
    """
    body = BodyStatisticsWelchTTest(series_1_id, series_2_id, alternative)
    result = operation.statistics_welch_t_test(body).additional_properties
    return result["t_statistic"], result["p_value"]


def wilcoxon_signed_rank_test(
    operation: SyncOperations, series_1_id: str, series_2_id: str, alternative: str
) -> Tuple[float, float]:
    """
    Calculates the Wilcoxon signed rank test of two sample series.
    Parameters
    ----------
    :param operation: Object used to reference fast_api_client function calls
    :type operation: SyncOperations
    :param series_1_id: The id of the series to be processed
    :type series_1_id: string
    :param series_2_id: The id of the series to be processed
    :type series_2_id: string
    :param alternative: The alternative used. May be "less", "two-sided" or "greater"
    :type alternative: string

    Returns
    -------
    float
       The w statistic of the sample series.
    float
       The p-value of the sample series.
    """
    body = BodyStatisticsWilcoxonSignedRankTest(series_1_id, series_2_id, alternative)
    result = operation.statistics_wilcoxon_signed_rank_test(body)
    return result["w_statistic"], result["p_value"]
