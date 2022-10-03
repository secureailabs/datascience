import math
from typing import Dict, List, Tuple, Type

import numpy as np
from sail_scn_lib.data import RemoteSeries
from scipy import stats


def chisquare(
    sample_0: Type[RemoteSeries],
    sample_1: Type[RemoteSeries],
) -> Dict:
    precompute = {}
    sample_0 = sample_0.series
    sample_1 = sample_1.series
    for tuple_value in zip(sample_0, sample_1):
        if tuple_value not in precompute:
            precompute[tuple_value] = 0
        precompute[tuple_value] = precompute[tuple_value] + 1
    return precompute


def chisquare_agg(
    list_precompute: List,
) -> Dict:
    list_unique_0 = []
    list_unique_1 = []
    for precompute in list_precompute:
        for tuple_value in precompute:
            value_0 = tuple_value[0]
            value_1 = tuple_value[1]
            if value_0 not in list_unique_0:
                list_unique_0.append(value_0)
            if value_1 not in list_unique_1:
                list_unique_1.append(value_1)

    array_true = np.zeros((len(list_unique_0), len(list_unique_1)))
    array_pred = np.zeros((len(list_unique_0), len(list_unique_1)))
    count_total = 0
    for precompute in list_precompute:
        for tuple_value in precompute:
            value_0 = tuple_value[0]
            value_1 = tuple_value[1]
            index_0 = list_unique_0.index(value_0)
            index_1 = list_unique_1.index(value_1)
            array_true[index_0, index_1] += precompute[tuple_value]
            count_total += precompute[tuple_value]

    for i_0 in range(array_true.shape[0]):
        for i_1 in range(array_true.shape[1]):
            array_pred[i_0, i_1] = array_true[i_0, :].sum() * array_true[:, i_1].sum() / count_total

    array_true = array_true.ravel()
    array_pred = array_pred.ravel()
    chisquare_statistic = (np.power(array_true - array_pred, 2) / array_pred).sum()
    degrees_of_freedom = (len(list_unique_0) - 1) * (len(list_unique_1) - 1)

    p_value = stats.distributions.chi2.sf(chisquare_statistic, degrees_of_freedom)
    return (chisquare_statistic, p_value)


def kolmogorov_smirnovdef(
    sample_0: Type[RemoteSeries],
    sample_ranked_0: tuple,
    distribution: str,
    count_total: int,
) -> List[float]:
    type_distribution = distribution["type_distribution"]

    array_sample_0 = sample_0.series.to_numpy()
    array_sample_ranked_0 = np.array(sample_ranked_0)

    if type_distribution == "normal":
        sample_mean = np.mean(array_sample_0)
        sample_sdev = np.std(array_sample_0, ddof=1)
        array_value_cdf = stats.norm.cdf(array_sample_0, loc=sample_mean, scale=sample_sdev)
    elif type_distribution == "normalunit":
        array_value_cdf = stats.norm.cdf(array_sample_0, loc=0, scale=1)
    else:
        raise Exception()
    return np.max(np.abs((array_sample_ranked_0 / count_total) - array_value_cdf))


def kolmogorov_smirnovdef_agg(
    list_precompute: List[float],
) -> float:
    list_max = []
    for precompute in list_precompute:
        list_max.append(precompute)

    return max(list_max)


def levene(
    sample_0_series: Type[RemoteSeries],
    sample_1_series: Type[RemoteSeries],
    mean_0: float,
    mean_1: float,
) -> Tuple[List[float], List[bool]]:  # there seems to be a problem here with this annotation
    """
    ----------
    sample_0_series : pd.Series
        The series for sample_0
    sample_1_series : pd.Series
        The series for sample_1
    Returns
    -------
    a list of 6 floats, two moments for sample_0 followed by the size of sample_0 and two moments for sample_1 followed by the size of sample 1
    """

    sample_0 = sample_0_series.series.to_numpy()
    sample_1 = sample_1_series.series.to_numpy()

    sum_x_0 = float(np.sum(sample_0))
    sum_xx_0 = float(np.sum(sample_0 * sample_0))
    count_0 = len(sample_0)

    sum_x_1 = float(np.sum(sample_1))
    sum_xx_1 = float(np.sum(sample_1 * sample_1))
    count_1 = len(sample_1)

    # is it safe to pass these two?
    z1j = abs(sample_0 - mean_0)
    z1j = z1j.tolist()
    z2j = abs(sample_1 - mean_1)
    z2j = z2j.tolist()

    list_precompute = [sum_x_0, sum_xx_0, count_0, sum_x_1, sum_xx_1, count_1, z1j, z2j]

    return list_precompute


def levene_agg(
    list_list_precompute: List[List[float]],
    equal_varriances: bool = False,
) -> Tuple[float, float]:
    sum_x_0 = 0
    sum_xx_0 = 0
    size_sample_0 = 0
    sum_x_1 = 0
    sum_xx_1 = 0
    size_sample_1 = 0
    final_z1j = []
    final_z2j = []
    for list_precompute in list_list_precompute:
        sum_x_0 += list_precompute[0]
        sum_xx_0 += list_precompute[1]
        size_sample_0 += list_precompute[2]
        sum_x_1 += list_precompute[3]
        sum_xx_1 += list_precompute[4]
        size_sample_1 += list_precompute[5]
        final_z1j.extend(list_precompute[6])
        final_z2j.extend(list_precompute[7])

    z1_ = np.mean(final_z1j)
    z2_ = np.mean(final_z2j)

    z__ = (z1_ + z2_) / 2

    denom_1 = final_z1j - z1_
    denom_1 = np.sum(denom_1 * denom_1)

    denom_2 = final_z2j - z2_
    denom_2 = np.sum(denom_2 * denom_2)

    final_denom = denom_1 + denom_2
    length1 = size_sample_0
    length2 = size_sample_1
    dof = length1 + length2 - 2
    final_nem = dof * (length1 * (z1_ - z__) * (z1_ - z__) + length2 * (z2_ - z__) * (z2_ - z__))

    f_statictic = float(final_nem / final_denom)

    return (f_statictic, dof)


def mann_whitney(
    series_0: Type[RemoteSeries],
    series_concatenated_ranked: tuple,
) -> float:
    series_concatenated_ranked = np.array(series_concatenated_ranked)
    return series_concatenated_ranked[: series_0.size].sum()


def mann_whitney_agg(list_precompute: List[float]) -> float:
    return np.array(list_precompute).sum()


def paired_t(
    sample_0_series: Type[RemoteSeries],
    sample_1_series: Type[RemoteSeries],
) -> List[float]:
    """Generates the geometric moments for use in a T-Test
    :param sample_0_series:  The series for sample_0
    :type sample_0_series: pd.Series
    :param sample_1_series: The series for sample_1
    :type sample_1_series: pd.Series
    :return: a list of 3 floats, two moments for sample_d followed by the size of sample_d
    :rtype: List[float]
    """

    sample_0 = sample_0_series.series.to_numpy()
    sample_1 = sample_1_series.series.to_numpy()
    sample_d = sample_0 - sample_1
    sum_d_0 = np.sum(sample_d)
    sum_dd_0 = np.sum(sample_d * sample_d)
    count_d = len(sample_d)

    list_precompute = [sum_d_0, sum_dd_0, count_d]

    return list_precompute


def paired_t_agg(
    list_list_precompute: List[List[float]],
) -> Tuple[float, float]:
    """collects the parts of a t-test and agregates them into statisitcs
    :param list_list_precompute: a list of 3 floats; two moments for sample_d followed by the size of paired sample
    :type list_list_precompute: List[List[float]]
    :return: returns a t-statistic and its effect size
    :rtype: Tuple[float, float]
    """
    sum_d_0 = 0
    sum_dd_0 = 0
    size_sample_d = 0

    for list_precompute in list_list_precompute:
        sum_d_0 += list_precompute[0]
        sum_dd_0 += list_precompute[1]
        size_sample_d += list_precompute[2]

    sample_mean_d = sum_d_0 / size_sample_d
    sample_varriance_d = ((sum_dd_0 / size_sample_d) - (sample_mean_d * sample_mean_d)) * (
        size_sample_d / (size_sample_d - 1)  # unbiased estimator (numpy version is biased by default)
    )

    t_statistic = sample_mean_d / (np.sqrt(sample_varriance_d) / np.sqrt(size_sample_d))
    degrees_of_freedom = size_sample_d - 1

    # TODO we need to enable this when error handling is implemented
    # if degrees_of_freedom < 20:
    #     raise Exception()
    return (t_statistic, degrees_of_freedom)


def unpaired_t(
    sample_0_series: Type[RemoteSeries],
    sample_1_series: Type[RemoteSeries],
) -> List[float]:
    """Generates the geometric moments for use in a T-Test
    Parameters
    ----------
    sample_0_series : pd.Series
        The series for sample_0
    sample_1_series : pd.Series
        The series for sample_1
    Returns
    -------
    a list of 6 floats, two moments for sample_0 followed by the size of sample_0 and two moments for sample_1 followed by the size of sample 1
    """
    sample_0 = sample_0_series.series.to_numpy()
    sample_1 = sample_1_series.series.to_numpy()

    sum_x_0 = np.sum(sample_0)
    sum_xx_0 = np.sum(sample_0 * sample_0)
    count_0 = len(sample_0)

    sum_x_1 = np.sum(sample_1)
    sum_xx_1 = np.sum(sample_1 * sample_1)
    count_1 = len(sample_1)

    list_precompute = [sum_x_0, sum_xx_0, count_0, sum_x_1, sum_xx_1, count_1]

    return list_precompute


# def unpaired_t_agg(
#     list_list_precompute: List[List[float]],
#     equal_varriances: bool = False,
# ) -> Tuple[float, float]:
#     sum_x_0 = 0
#     sum_xx_0 = 0
#     size_sample_0 = 0
#     sum_x_1 = 0
#     sum_xx_1 = 0
#     size_sample_1 = 0
#     for list_precompute in list_list_precompute:
#         sum_x_0 += list_precompute[0]
#         sum_xx_0 += list_precompute[1]
#         size_sample_0 += list_precompute[2]
#         sum_x_1 += list_precompute[3]
#         sum_xx_1 += list_precompute[4]
#         size_sample_1 += list_precompute[5]

#     sample_mean_0 = sum_x_0 / size_sample_0
#     sample_varriance_0 = ((sum_xx_0 / size_sample_0) - (sample_mean_0 * sample_mean_0)) * (
#         size_sample_0 / (size_sample_0 - 1)  # unbiased estimator (numpy version is biased by default)
#     )

#     sample_mean_1 = sum_x_1 / size_sample_1
#     sample_varriance_1 = ((sum_xx_1 / size_sample_1) - (sample_mean_1 * sample_mean_1)) * (
#         size_sample_1 / (size_sample_1 - 1)  # unbiased estimator (np version is biased by default)
#     )

#     if equal_varriances:
#         sample_varriance_pooled = (
#             ((size_sample_0 - 1) * sample_varriance_0) + ((size_sample_1 - 1) * sample_varriance_1)
#         ) / (size_sample_0 + size_sample_1 - 2)
#         t_statistic = (sample_mean_0 - sample_mean_1) / (
#             np.sqrt(sample_varriance_pooled) * np.sqrt((1 / size_sample_0 + 1 / size_sample_1))
#         )
#         degrees_of_freedom = size_sample_0 + size_sample_1 - 2

#     else:
#         # sample_varriance_0 /= size_sample_0 / (size_sample_0 - 1)
#         # sample_varriance_1 /= size_sample_1 / (size_sample_1 - 1)
#         t_statistic = (sample_mean_0 - sample_mean_1) / (
#             np.sqrt((sample_varriance_0 / size_sample_0) + (sample_varriance_1 / size_sample_1))
#         )
#         # Welch–Satterthwaite equation:
#         dof_nominator = math.pow(((sample_varriance_0 / size_sample_0) + (sample_varriance_1 / size_sample_1)), 2)
#         dof_denominator = (math.pow(sample_varriance_0, 2) / (size_sample_0 * size_sample_0 * (size_sample_0 - 1))) + (
#             math.pow(sample_varriance_1, 2) / (size_sample_1 * size_sample_1 * (size_sample_1 - 1))
#         )
#         degrees_of_freedom = dof_nominator / dof_denominator

#     # if degrees_of_freedom < 20:
#     #     raise Exception()
#     return (t_statistic, degrees_of_freedom)


def student_t_agg(
    list_list_precompute: List[List[float]],
) -> Tuple:
    sum_x_0 = 0
    sum_xx_0 = 0
    size_sample_0 = 0
    sum_x_1 = 0
    sum_xx_1 = 0
    size_sample_1 = 0
    for list_precompute in list_list_precompute:
        sum_x_0 += list_precompute[0]
        sum_xx_0 += list_precompute[1]
        size_sample_0 += list_precompute[2]
        sum_x_1 += list_precompute[3]
        sum_xx_1 += list_precompute[4]
        size_sample_1 += list_precompute[5]

    sample_mean_0 = sum_x_0 / size_sample_0
    sample_variance_0 = ((sum_xx_0 / size_sample_0) - (sample_mean_0 * sample_mean_0)) * (
        size_sample_0 / (size_sample_0 - 1)  # unbiased estimator (numpy version is biased by default)
    )

    sample_mean_1 = sum_x_1 / size_sample_1
    sample_variance_1 = ((sum_xx_1 / size_sample_1) - (sample_mean_1 * sample_mean_1)) * (
        size_sample_1 / (size_sample_1 - 1)  # unbiased estimator (np version is biased by default)
    )

    sample_variance_pooled = (((size_sample_0 - 1) * sample_variance_0) + ((size_sample_1 - 1) * sample_variance_1)) / (
        size_sample_0 + size_sample_1 - 2
    )
    t_statistic = (sample_mean_0 - sample_mean_1) / (
        np.sqrt(sample_variance_pooled) * np.sqrt((1 / size_sample_0 + 1 / size_sample_1))
    )
    degrees_of_freedom = size_sample_0 + size_sample_1 - 2

    return t_statistic, degrees_of_freedom


def welch_t_agg(
    list_list_precompute: List[List[float]],
) -> Tuple:
    sum_x_0 = 0
    sum_xx_0 = 0
    size_sample_0 = 0
    sum_x_1 = 0
    sum_xx_1 = 0
    size_sample_1 = 0
    for list_precompute in list_list_precompute:
        sum_x_0 += list_precompute[0]
        sum_xx_0 += list_precompute[1]
        size_sample_0 += list_precompute[2]
        sum_x_1 += list_precompute[3]
        sum_xx_1 += list_precompute[4]
        size_sample_1 += list_precompute[5]

    sample_mean_0 = sum_x_0 / size_sample_0
    sample_variance_0 = ((sum_xx_0 / size_sample_0) - (sample_mean_0 * sample_mean_0)) * (
        size_sample_0 / (size_sample_0 - 1)  # unbiased estimator (numpy version is biased by default)
    )

    sample_mean_1 = sum_x_1 / size_sample_1
    sample_variance_1 = ((sum_xx_1 / size_sample_1) - (sample_mean_1 * sample_mean_1)) * (
        size_sample_1 / (size_sample_1 - 1)  # unbiased estimator (np version is biased by default)
    )

    t_statistic = (sample_mean_0 - sample_mean_1) / (
        np.sqrt((sample_variance_0 / size_sample_0) + (sample_variance_1 / size_sample_1))
    )
    # Welch–Satterthwaite equation:
    degrees_of_freedom_numerator = math.pow(
        ((sample_variance_0 / size_sample_0) + (sample_variance_1 / size_sample_1)),
        2,
    )
    degrees_of_freedom_denominator = (
        math.pow(sample_variance_0, 2) / (size_sample_0 * size_sample_0 * (size_sample_0 - 1))
    ) + (math.pow(sample_variance_1, 2) / (size_sample_1 * size_sample_1 * (size_sample_1 - 1)))
    degrees_of_freedom = degrees_of_freedom_numerator / degrees_of_freedom_denominator

    return t_statistic, degrees_of_freedom


def wilcoxon_signed_rank(
    sample_difference: Type[RemoteSeries],
    sample_absolute_difference_ranked: tuple,
) -> List[float]:
    rank_minus = np.sum((sample_difference.series.to_numpy() < 0) * np.array(sample_absolute_difference_ranked))
    rank_plus = np.sum((sample_difference.series.to_numpy() > 0) * np.array(sample_absolute_difference_ranked))
    return [rank_minus, rank_plus]


def wilcoxon_signed_rank_agg(
    list_precompute: List,
) -> Tuple[float]:
    rank_minus = 0
    rank_plus = 0
    for precompute in list_precompute:
        rank_minus += precompute[0]
        rank_plus += precompute[1]
    return (rank_minus, rank_plus)
