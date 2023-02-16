import json
from typing import Dict

import numpy
import pandas as pd
from sail_safe_functions.aggregator.series import Series
from sail_safe_functions.aggregator.series_federated import SeriesFederated


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


def check_series_paired(series_0: SeriesFederated, series_1: SeriesFederated) -> None:
    # TODO this avoids a serial import but it should move
    from sail_safe_functions.aggregator import statistics

    size_0 = statistics.count(series_0)
    size_1 = statistics.count(series_1)
    if size_0 != size_1:
        # TODO check the indexes for matching
        raise ValueError("`sample_0` and `sample_1` must have the same length.")


def check_series_empty_federated(series: SeriesFederated) -> None:
    # TODO this avoids a serial import but it should move
    from sail_safe_functions.aggregator import statistics

    if statistics.count(series) == 0:
        raise Exception("series cannot be empty")


def check_series_one_value_federated(series: SeriesFederated) -> None:
    # TODO this avoids a serial import but it should move
    from sail_safe_functions.aggregator import statistics

    if statistics.count(series) == 1:
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
