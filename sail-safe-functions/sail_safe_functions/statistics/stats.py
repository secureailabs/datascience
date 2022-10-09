import math
from typing import List, Tuple, Type

import numpy as np
from sail_safe_functions.data import RemoteSeries


def mean(
    sample_0_dataframe: Type[RemoteSeries],
) -> Tuple[float, int]:  # there seems to be a problem here with this annotation
    sample_0 = sample_0_dataframe.series.to_numpy()

    sum_x_0 = float(np.sum(sample_0))
    sample_0_dof = len(sample_0)

    list_precompute = [sum_x_0, sample_0_dof]
    # list_safe = [False, False, False, False, False, False ]
    return list_precompute


def mean_agg(
    list_list_precompute: List[List[float]],
) -> float:
    sum_x_0 = 0
    dof_0 = 0

    for list_precompute in list_list_precompute:
        sum_x_0 += list_precompute[0]
        dof_0 += list_precompute[1]

    sample_mean_0 = sum_x_0 / dof_0

    # if degrees_of_freedom < 20:
    #     raise Exception()
    return sample_mean_0


def min_max(
    series_sample: Type[RemoteSeries],
) -> Tuple[float, float]:
    """This function is designed to counteract disclosure of the min and max while giving them estimates that
    are independant for sample size bigger than 2. The function guarantees that min <= sample_min and sample_max <= max
    For uniform distributions this follows the UMVU-estimator altough with bigger varriance
    For normal distribution this creates a min and a max that are far outside the sample
    min and max to protect outliers.
    TODO this function can be improved by doing the actual estimation in the agregate section
    :param series_sample: the sample from witch to estimate the min and max
    :type series_sample: pd.Series
    :raises ValueError: raises a ValueError if the series contains `na` values
    :return: The min and max estimate from the series
    :rtype: Tuple[float, float]
    """
    series_sample = series_sample.series
    if 0 < series_sample.isna().sum():
        raise ValueError("Sample contains `na` values")
    array_sample = np.array(series_sample.sort_values(ascending=True, inplace=False))
    subsample_size = int(np.ceil(np.sqrt(series_sample.size)))
    subsample_min = array_sample[:subsample_size]
    subsample_max = array_sample[-subsample_size:]
    subsample_min_width = np.max(subsample_min) - np.min(subsample_min)
    estimate_min = np.min(subsample_min) - (subsample_min_width**2 / series_sample.size)
    subsample_max_width = np.max(subsample_max) - np.min(subsample_max)
    estimate_max = np.max(subsample_max) + (subsample_max_width**2 / series_sample.size)
    return (estimate_min, estimate_max)


def min_max_agg(
    list_tuple_min_max: List[Tuple[float, float]],
) -> Tuple[float, float]:
    """Agregates the results of multiple precompute functions into a global min and max
    :param list_tuple_min_max: A list of tuples from various precompute functions
    :type list_tuple_min_max: List[Tuple[float, float]]
    :return: return the federated estimated sample min max
    :rtype: Tuple[float, float]
    """
    list_min = []
    list_max = []
    for tuple_min_max in list_tuple_min_max:
        list_min.append(tuple_min_max[0])
        list_max.append(tuple_min_max[1])
    return (min(list_min), max(list_max))


def skewness(
    sample_0_dataframe: Type[RemoteSeries],
) -> List[float]:
    """Generates the geometric moments for use in a Skewness
    Parameters
    ----------
    sample_0_dataframe : pd.DataFrame
        The dataframe for sample_0
    Returns
    -------
    a list of 3 floats precompute value
    """

    sample_0 = sample_0_dataframe.series.to_numpy()
    # First
    sum_x_0 = np.sum(sample_0)
    # second
    sum_xx_0 = np.sum(sample_0 * sample_0)
    # Third
    sum_xxx_0 = np.sum(sample_0 * sample_0 * sample_0)
    # Sample size
    count_0 = len(sample_0)

    list_precompute = [sum_x_0, sum_xx_0, sum_xxx_0, count_0]

    return list_precompute


def skewness_agg(
    list_list_precompute: List[List[float]],
) -> float:

    """
    A Function to get the fedrated skewness value.
    same as scipy.skewsnes ()
    :param list_list_precompute: compute from different DF
    :type list_list_precompute: List[List[float]]
    :return: Skewness Value
    :rtype: Float
    """

    sum_x_0 = 0
    sum_xxx_0 = 0
    sum_xx_0 = 0
    size_sample_0 = 0
    # Combining precompute
    for list_precompute in list_list_precompute:
        sum_x_0 += list_precompute[0]
        sum_xx_0 += list_precompute[1]
        sum_xxx_0 += list_precompute[2]
        size_sample_0 += list_precompute[3]  # same as Count_0

    # Calculating sampel mean
    sample_mean_0 = sum_x_0 / size_sample_0
    # Calculating sample varriance
    sample_varriance_0 = (sum_xx_0 / size_sample_0) - (sample_mean_0 * sample_mean_0)
    # Calculating Sample
    sample_standard_deviation = math.sqrt(sample_varriance_0)
    # mu3 Geometric
    mu3 = sum_xxx_0 / size_sample_0
    mean = sample_mean_0
    sd = sample_standard_deviation
    # Final Statistical formula for calculating skewness
    # wiki link below for the formula
    # https://en.wikipedia.org/wiki/Skewness
    skewness_value = (mu3 - (3 * mean * sd * sd) - mean**3) / (sd**3)

    return skewness_value


def pearson(
    sample_0_dataframe: Type[RemoteSeries],
    sample_1_dataframe: Type[RemoteSeries],
) -> List[float]:
    """
    Parameters
    ----------
    sample_0_dataframe : pd.DataFrame
        The dataframe for sample_0
    sample_1_dataframe : pd.DataFrame
        The dataframe for sample_1
    Returns
    -------
    a list of 6 floats
    """
    sample_0 = None
    sample_1 = None
    if isinstance(sample_0_dataframe, RemoteSeries):
        sample_0 = sample_0_dataframe.series.to_numpy()
    elif isinstance(sample_0_dataframe, tuple):
        sample_0 = np.array(sample_0_dataframe)
    else:
        sample_0 = sample_0_dataframe
    if isinstance(sample_1_dataframe, RemoteSeries):
        sample_1 = sample_1_dataframe.series.to_numpy()
    elif isinstance(sample_1_dataframe, tuple):
        sample_1 = np.array(sample_1_dataframe)
    else:
        sample_1 = sample_1_dataframe

    sum_x_0 = float(np.sum(sample_0))
    sum_xx_0 = float(np.sum(sample_0 * sample_0))
    sample_0_dof = len(sample_0)

    sum_x_1 = float(np.sum(sample_1))
    sum_xx_1 = float(np.sum(sample_1 * sample_1))
    sample_1_dof = len(sample_1)

    sum_x1_into_x2 = float(np.sum(np.multiply(sample_0, sample_1)))

    list_precompute = [sum_x_0, sum_xx_0, sample_0_dof, sum_x_1, sum_xx_1, sample_1_dof, sum_x1_into_x2]

    # list_safe = [False, False, False, False, False, False ]
    return list_precompute


def pearson_agg(
    list_list_precompute: List[List[float]],
) -> Tuple[float, int]:
    """
    This function run to calculate the final precompute
    and calculate the federated pearson value.
    :param list_list_precompute:
    :type list_list_precompute: List[List[float]]
    :return: Pearson value r
    :rtype: float
    """
    sum_x_0 = 0
    sum_x_1 = 0
    sum_xx_0 = 0
    sum_xx_1 = 0
    sum_x1_into_x2 = 0
    size_sample_0 = 0
    size_sample_1 = 0
    for list_precompute in list_list_precompute:
        sum_x_0 += list_precompute[0]
        sum_xx_0 += list_precompute[1]
        size_sample_0 += list_precompute[2]
        sum_x_1 += list_precompute[3]
        sum_xx_1 += list_precompute[4]
        size_sample_1 += list_precompute[5]
        sum_x1_into_x2 += list_precompute[6]

    # Calculating for the first column
    # Calculating sampel mean
    sample_mean_0 = sum_x_0 / size_sample_0
    # Calculating sample varriance
    sample_varriance_0 = (sum_xx_0 / size_sample_0) - (sample_mean_0 * sample_mean_0)
    # Calculating Sample
    sample_standard_deviation_0 = math.sqrt(sample_varriance_0)
    # Calculating for the second column
    # Calculating sampel mean
    sample_mean_1 = sum_x_1 / size_sample_1
    # Calculating sample varriance
    sample_varriance_1 = (sum_xx_1 / size_sample_1) - (sample_mean_1 * sample_mean_1)
    # Calculating Sample
    sample_standard_deviation_1 = math.sqrt(sample_varriance_1)

    E_xy = sum_x1_into_x2 / size_sample_0

    rho = (E_xy - (sample_mean_0 * sample_mean_1)) / (sample_standard_deviation_0 * sample_standard_deviation_1)
    degrees_of_freedom = size_sample_0 - 2
    return (rho, degrees_of_freedom)


def variance(
    sample_0: Type[RemoteSeries],
) -> Tuple[List[float], List[bool]]:  # there seems to be a problem here with this annotation
    sample_0 = sample_0.series.to_numpy()

    sum_x_0 = np.sum(sample_0)
    sum_xx_0 = np.sum(sample_0 * sample_0)
    sample_0_dof = len(sample_0)

    list_precompute = [sum_x_0, sum_xx_0, sample_0_dof]
    return list_precompute


def variance_agg(
    list_list_precompute: List[List[float]],
) -> float:
    sum_x_0 = 0
    sum_xx_0 = 0
    size_sample_0 = 0

    for list_precompute in list_list_precompute:
        sum_x_0 += list_precompute[0]
        sum_xx_0 += list_precompute[1]
        size_sample_0 += list_precompute[2]

    sample_mean_0 = sum_x_0 / size_sample_0

    sample_varriance_0 = ((sum_xx_0 / size_sample_0) - (sample_mean_0 * sample_mean_0)) * (
        size_sample_0 / (size_sample_0 - 1)  # unbiased estimator (numpy version is biased by default)
    )

    return sample_varriance_0


def kurtosis(
    sample_0_dataframe: Type[RemoteSeries],
) -> List[float]:
    """Generates the geometric moments for use in a Kurtosis
    Parameters
    ----------
    sample_0_dataframe : pd.DataFrame
        The dataframe for sample_0
    Returns
    -------
    a list of 3 floats precomputes value
    """

    sample_0 = sample_0_dataframe.series.to_numpy()
    # First
    sum_x_0 = np.sum(sample_0)
    # second
    sum_xx_0 = np.sum(sample_0 * sample_0)
    # Third
    sum_xxx_0 = np.sum(sample_0 * sample_0 * sample_0)
    # Fourth
    sum_xxxx_0 = np.sum(sample_0 * sample_0 * sample_0 * sample_0)
    # Sample size
    count_0 = len(sample_0)

    list_precompute = [sum_x_0, sum_xx_0, sum_xxx_0, sum_xxxx_0, count_0]

    return list_precompute


def kurtosis_agg(
    list_list_precompute: List[List[float]],
) -> float:

    """
    A Function to get the fedrated Kurtosis value.
    same as scipy.skewsnes ()
    :param list_list_precompute: compute from different DF
    :type list_list_precompute: List[List[float]]
    :return: Kurtosis Value
    :rtype: Float
    """

    sum_x_0 = 0
    sum_xx_0 = 0
    sum_xxx_0 = 0
    sum_xxxx_0 = 0
    size_sample_0 = 0
    # Combining precompute
    for list_precompute in list_list_precompute:
        sum_x_0 += list_precompute[0]
        sum_xx_0 += list_precompute[1]
        sum_xxx_0 += list_precompute[2]
        sum_xxxx_0 += list_precompute[3]
        size_sample_0 += list_precompute[4]  # same as Count_0

    # Calculating sampel mean
    sample_mean_0 = sum_x_0 / size_sample_0
    # Calculating sample varriance
    sample_varriance_0 = (sum_xx_0 / size_sample_0) - (sample_mean_0 * sample_mean_0)
    # Calculating Sample
    sample_standard_deviation = math.sqrt(sample_varriance_0)

    # mu Geometric
    mu2 = sum_xx_0 / size_sample_0
    mu3 = sum_xxx_0 / size_sample_0
    mu4 = sum_xxxx_0 / size_sample_0
    mean = sample_mean_0
    sd = sample_standard_deviation

    # Final Statistical formula for calculating Kurtosis
    # wiki link below for the formula
    # https://en.wikipedia.org/wiki/Kurtosis

    kurtosis_value = ((mu4) - 3 * (mean**4) - 4 * ((mu3) * (mean)) + 6 * ((mu2) * (mean**2))) / (sd**4)

    return kurtosis_value - 3
