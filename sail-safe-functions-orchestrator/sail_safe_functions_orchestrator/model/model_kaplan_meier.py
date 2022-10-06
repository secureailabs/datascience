from typing import Dict

import matplotlib.pyplot as plt
import numpy
import pandas
import scipy
from lifelines import KaplanMeierFitter
from sail_safe_functions.statistics.survival_curve_kaplan_meier_agregate import SurvivalCurveKaplanMeierAgregate
from sail_safe_functions.statistics.survival_curve_kaplan_meier_precompute import SurvivalCurveKaplanMeierPrecompute
from sail_safe_functions_orchestrator import preprocessing, visualization
from sail_safe_functions_orchestrator.data_frame_federated import DataFrameFederated


class ModelKaplanMeier:
    def __init__(self) -> None:
        super().__init__()
        self.count_total = 0
        self.count_observed = 0
        self.domain = []
        self.mean = []
        self.lower = []
        self.upper = []

    def fit(
        self, data_frame_source: DataFrameFederated, name_feature_duration: str, name_feature_observation: str
    ) -> None:
        # TODO check name_feature_duration is float?
        # TODO check name_feature_observation is boolean?
        # alternitive 1
        list_survival_curve_dict = []
        for dataset_id in data_frame_source.dict_dataframe:
            list_survival_curve_dict.append(
                SurvivalCurveKaplanMeierPrecompute.run(
                    data_frame_source.dict_dataframe[dataset_id], name_feature_duration, name_feature_observation
                )
            )
        survival_curve_dict = SurvivalCurveKaplanMeierAgregate.run(list_survival_curve_dict)

        # alternitive 2
        self.count_total = survival_curve_dict["count_total"]
        self.count_observed = survival_curve_dict["count_observed"]

        self.domain = survival_curve_dict["domain"]
        self.mean = survival_curve_dict["mean"]
        self.lower = survival_curve_dict["lower"]
        self.upper = survival_curve_dict["upper"]

    def compute_hazard(self, ratio_reference: float, time_point: float) -> Dict:

        hazard = {}
        if self.domain[-1] < time_point:
            # TODO this is a bit shit, the confidence interval is 0 now which is wrong
            # Also we can extrapolate better
            hazzard_ratio_mean = ratio_reference / (1 - (self.count_observed / self.count_total))
            hazzard_ratio_lower = hazzard_ratio_mean
            hazzard_ratio_upper = hazzard_ratio_mean
        else:
            hazzard_ratio_mean = ratio_reference / scipy.interpolate.interp1d(self.domain, self.mean)(time_point)
            # lower and upper are swapped due to division
            hazzard_ratio_upper = ratio_reference / scipy.interpolate.interp1d(self.domain, self.lower)(time_point)
            hazzard_ratio_lower = ratio_reference / scipy.interpolate.interp1d(self.domain, self.upper)(time_point)

        if hazzard_ratio_mean == numpy.inf:
            # TODO this is a bit shit, the confidence interval is 0 now which is wrong
            hazzard_ratio_mean = 1.0
            hazzard_ratio_lower = 1.0
            hazzard_ratio_upper = 1.0
            is_default = True
        else:
            is_default = False
        hazard = {}
        hazard["survival_curve"] = self.get_survival_curve_dict()
        hazard["count_total"] = self.count_total
        hazard["count_observed"] = self.count_observed
        hazard["is_default"] = is_default
        hazard["hazzard_ratio_mean"] = hazzard_ratio_mean
        hazard["hazzard_ratio_lower"] = hazzard_ratio_lower
        hazard["hazzard_ratio_upper"] = hazzard_ratio_upper
        return hazard

    def get_survival_curve_dict(self) -> Dict:
        survival_curve_dict = {}
        survival_curve_dict["count_total"] = self.count_total
        survival_curve_dict["count_observed"] = self.count_observed
        survival_curve_dict["domain"] = self.domain
        survival_curve_dict["mean"] = self.mean
        survival_curve_dict["lower"] = self.lower
        survival_curve_dict["upper"] = self.upper
        return survival_curve_dict

    @staticmethod
    def plot(
        data_frame_source: DataFrameFederated, name_feature_duration, name_feature_observation, name_feature_group: str
    ):
        figure, axes = plt.subplots(figsize=(15, 8), dpi=80)
        list_name_value = pandas.unique(data_frame_source.to_pandas()[name_feature_group])  # TODO use schema
        for name_value in list_name_value:
            data_frame_target = preprocessing.select_column(
                data_frame_source, [name_feature_duration, name_feature_observation, name_feature_group]
            )
            data_frame_hazard = preprocessing.query(data_frame_target, f"(`{name_feature_group}` == '{name_value}')")
            # data_frame_hazard = data_frame_hazard[data_frame_target[name_feature_observation].notna()]

            model_kaplan_meier = ModelKaplanMeier()
            model_kaplan_meier.fit(data_frame_hazard, name_feature_duration, name_feature_observation)
            survival_curve = model_kaplan_meier.get_survival_curve_dict()
            count_observed = survival_curve["count_observed"]
            count_total = survival_curve["count_total"]
            name_series = f"{name_value} (N={count_observed}/{count_total})"
            visualization.plot_survival_curve(axes, survival_curve, name_series)
        plt.legend()
        plt.ylabel("survival faction")
        plt.xlabel("name_feature_duration")
        plt.title(name_feature_group)
        plt.show()
        return figure
