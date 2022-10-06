import math
from typing import Dict, List

import numpy
import pandas
from lifelines import KaplanMeierFitter


class SurvivalCurveKaplanMeierPrecompute:
    def run(data_frame: pandas.DataFrame, name_feature_duration: str, name_feature_observation: str) -> Dict:
        if data_frame.shape[0] == 0:
            # Empty dataframe exception
            survival_curve_dict = {}
            survival_curve_dict["count_total"] = 0
            survival_curve_dict["count_observed"] = 0
            survival_curve_dict["domain"] = []
            survival_curve_dict["mean"] = []
            survival_curve_dict["lower"] = []
            survival_curve_dict["upper"] = []
            return survival_curve_dict

        count_total = data_frame[name_feature_observation].count()
        count_observed = data_frame[name_feature_observation].sum()

        kmf = KaplanMeierFitter()
        kmf.fit(data_frame[name_feature_duration], data_frame[name_feature_observation])

        domain = kmf.survival_function_.index.to_numpy()
        mean = kmf.survival_function_.to_numpy()[:, 0]
        lower = kmf.confidence_interval_survival_function_.to_numpy()[:, 0]
        upper = kmf.confidence_interval_survival_function_.to_numpy()[:, 1]

        survival_curve_dict = {}
        survival_curve_dict["count_total"] = count_total
        survival_curve_dict["count_observed"] = count_observed
        survival_curve_dict["domain"] = domain
        survival_curve_dict["mean"] = mean
        survival_curve_dict["lower"] = lower
        survival_curve_dict["upper"] = upper
        return survival_curve_dict
