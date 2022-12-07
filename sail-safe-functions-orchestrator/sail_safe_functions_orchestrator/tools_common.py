import json
from typing import Dict

import numpy
import pandas as pd
from sail_safe_functions_orchestrator.series import Series


def check_instance(instance, class_check) -> None:
    if not isinstance(instance, class_check):
        raise Exception(f"{instance} is not instance of class: {class_check} instead type is {type(instance)}")


def check_series_nan(series: Series) -> None:
    series = pd.Series(series)
    if 0 < series.isna().sum():
        raise Exception("series cannot containt nan or None values")


def check_empty_series(series: Series) -> None:
    if series.size == 0:
        raise Exception("series cannot be empty")


def check_series_one_value(series: Series) -> None:
    if series.size == 1:
        raise Exception("series cannot containt only one value")


def check_series_constant(series: Series) -> None:
    series = pd.Series(series)
    if 1 == series.nunique():
        raise Exception("input array is constant")


def check_variance_zero(value) -> None:
    if value == 0:
        raise Exception("Variance is zero raises sys.float_info.max ")


def sanitize_dict_for_json(dict_in: Dict) -> Dict:
    class NpEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, numpy.integer):
                return int(obj)
            if isinstance(obj, numpy.floating):
                return float(obj)
            if isinstance(obj, numpy.ndarray):
                return obj.tolist()
            return super(NpEncoder, self).default(obj)

    return json.loads(json.dumps(dict_in, cls=NpEncoder))
