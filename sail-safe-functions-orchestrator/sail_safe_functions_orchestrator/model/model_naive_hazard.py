from typing import Dict

import numpy
import pandas
import scipy
from lifelines import KaplanMeierFitter
from sail_safe_functions_orchestrator.model.model_base import ModelBase
from sail_safe_functions_orchestrator.schema_date_frame import SchemaDataFrame


class ModelNaiveHazard(ModelBase):
    def __init__(
        self,
    ) -> None:
        super().__init__()
        self.name_feature_duration = ""
        self.name_feature_observation = ""
        self.dict_dict_hazard = {}

    @staticmethod
    def fit_kaplan_meier(data_frame: pandas.DataFrame, name_feature_duration: str, name_feature_observation: str):
        # TODO check name_feature_duration is float?
        # TODO check name_feature_observation is boolean?

        count_total = data_frame[name_feature_observation].count()
        count_observed = data_frame[name_feature_observation].sum()
        kmf = KaplanMeierFitter()
        kmf.fit(data_frame[name_feature_duration], data_frame[name_feature_observation])

        fraction_observed = data_frame[name_feature_observation].sum() / data_frame[name_feature_observation].shape[0]
        domain = kmf.survival_function_.index.to_numpy()
        mean = kmf.survival_function_.to_numpy()[:, 0] * fraction_observed + (1 - fraction_observed)
        lower = kmf.confidence_interval_survival_function_.to_numpy()[:, 0] * fraction_observed + (
            1 - fraction_observed
        )
        upper = kmf.confidence_interval_survival_function_.to_numpy()[:, 1] * fraction_observed + (
            1 - fraction_observed
        )

        kaplan_meier_fit = {}
        kaplan_meier_fit["count_total"] = count_total
        kaplan_meier_fit["count_observed"] = count_observed
        kaplan_meier_fit["domain"] = domain
        kaplan_meier_fit["mean"] = mean
        kaplan_meier_fit["lower"] = lower
        kaplan_meier_fit["upper"] = upper
        return kaplan_meier_fit

    @staticmethod
    def compute_hazard(ratio_reference: float, kaplan_meier_fit: Dict, time_point: float):
        count_total = kaplan_meier_fit["count_total"]
        count_observed = kaplan_meier_fit["count_observed"]
        domain = kaplan_meier_fit["domain"]
        mean = kaplan_meier_fit["mean"]
        lower = kaplan_meier_fit["lower"]
        upper = kaplan_meier_fit["upper"]
        hazard = {}
        if domain[-1] < time_point:
            # TODO this is a bit shit, the confidence interval is 0 now which is wrong
            # Also we can extrapolate better
            hazzard_ratio_mean = ratio_reference / (1 - (count_observed / count_total))
            hazzard_ratio_lower = hazzard_ratio_mean
            hazzard_ratio_upper = hazzard_ratio_mean
        else:
            hazzard_ratio_mean = ratio_reference / scipy.interpolate.interp1d(domain, mean)(time_point)
            # lower and upper are swapped due to division
            hazzard_ratio_upper = ratio_reference / scipy.interpolate.interp1d(domain, lower)(time_point)
            hazzard_ratio_lower = ratio_reference / scipy.interpolate.interp1d(domain, upper)(time_point)

        if hazzard_ratio_mean == numpy.inf:
            # TODO this is a bit shit, the confidence interval is 0 now which is wrong
            hazzard_ratio_mean = 1.0
            hazzard_ratio_lower = 1.0
            hazzard_ratio_upper = 1.0
            is_default = True
        else:
            is_default = False
        hazard = {}
        hazard["kaplan_meier_fit"] = kaplan_meier_fit
        hazard["count_total"] = count_total
        hazard["count_observed"] = count_observed
        hazard["is_default"] = is_default
        hazard["hazzard_ratio_mean"] = hazzard_ratio_mean
        hazard["hazzard_ratio_lower"] = hazzard_ratio_lower
        hazard["hazzard_ratio_upper"] = hazzard_ratio_upper
        return hazard

    def add_feature_hazard(self, data_frame: pandas.DataFrame, name_feature_hazard: str, include_missing: bool):
        # TODO loop
        kaplan_meier_fit = ModelNaiveHazard.fit_kaplan_meier(
            data_frame, self.name_feature_duration, self.name_feature_observation
        )
        dict_hazard = {}
        hazard = ModelNaiveHazard.compute_hazard()
        self.dict_dict_hazard[name_feature_hazard] = dict_hazard

    def fit(
        self,
        data_frame: pandas.DataFrame,
        name_feature_duration: str,
        name_feature_observation: str,
        include_missing: bool = True,
    ) -> None:
        self.name_feature_duration = name_feature_duration
        self.name_feature_observation = name_feature_observation
        for name_feature in data_frame.columns:
            if name_feature not in [self.name_feature_duration, self.name_feature_observation]:
                self.add_feature_hazard(data_frame, name_feature, include_missing)

    def predict(self, data_frame: pandas.DataFrame, name_feature_score: str):
        list_score = []
        for index_row in range(data_frame.shape[0]):
            data_frame_row = data_frame.iloc[[index_row]]
            score = 1
            for name_feature, dict_hazard in self.dict_dict_hazard.items():
                value = data_frame_row[name_feature].values[0]
                if type(value) == float:
                    value = "missing"
                if value in dict_hazard:
                    hazard = dict_hazard[value]
                    score *= hazard["hazzard_ratio_mean"]
            list_score.append(score)
        data_frame[name_feature_score] = list_score
        return data_frame
