import math
from typing import Dict, List

import numpy
import pandas


def sum_dict_moment(list_dict_moment: List[Dict]) -> Dict:
    if len(list_dict_moment) == 0:
        return {}
    dict_moment = list_dict_moment[0].copy()
    for dict_moment_add in list_dict_moment[1:]:
        if list(dict_moment.keys()) != list(dict_moment_add.keys()):
            raise ValueError("Not all keys in dictionaries match")
        for key, value in dict_moment_add.items():
            dict_moment[key] += value
    return dict_moment


def compute_dict_geometric_moment(list_series: List[pandas.Series], list_code_moment):
    dict_moment = {}
    for code_moment in list_code_moment:
        dict_moment[code_moment] = compute_geometric_moment(list_series, code_moment)
    return dict_moment


def compute_geometric_moment(list_series: List[pandas.Series], code_moment: str):
    for series in list_series:
        if series.dtype != numpy.float64:
            raise Exception("Can only compute moments on float64 series")

        if series.isnull().values.any():
            raise Exception("Series cannot contain nan values")

    # TODO the better way to do this would be via a dataframe and index columns on there
    size_series = len(list_series[0])
    # split code into odd and even parts
    list_index = [int(code_part) for code_part in code_moment.split("_")[::2]]
    list_power = [float(code_part) for code_part in code_moment.split("_")[1::2]]
    moment = 0
    # TODO lots of speedup possible via vectorization
    for index_element in range(size_series):
        moment_add = 1
        for index_series, power in zip(list_index, list_power):

            moment_add *= math.pow(list_series[index_series][index_element], power)

        moment += moment_add

    return moment