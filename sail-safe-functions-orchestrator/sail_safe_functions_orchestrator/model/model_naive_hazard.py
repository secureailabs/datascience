from typing import Dict, List

import matplotlib.pyplot as plt
import numpy
import pandas
import scipy
from lifelines import KaplanMeierFitter
from sail_safe_functions_orchestrator import visualization
from sail_safe_functions_orchestrator.model.model_base import ModelBase


class ModelNaiveHazard(ModelBase):
    def __init__(self, time_point) -> None:
        super().__init__()
        self.list_name_feature_hazard = []
        self.name_feature_duration = ""
        self.name_feature_observation = ""
        self.dict_dict_hazard = {}
        self.time_point = time_point

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
        # mean = kmf.survival_function_.to_numpy()[:, 0] * fraction_observed + (1 - fraction_observed)
        # lower = kmf.confidence_interval_survival_function_.to_numpy()[:, 0] * fraction_observed + (
        #     1 - fraction_observed
        # )
        # upper = kmf.confidence_interval_survival_function_.to_numpy()[:, 1] * fraction_observed + (
        #     1 - fraction_observed
        # )

        mean = kmf.survival_function_.to_numpy()[:, 0]
        lower = kmf.confidence_interval_survival_function_.to_numpy()[:, 0]
        upper = kmf.confidence_interval_survival_function_.to_numpy()[:, 1]

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
        hazard["survival_curve"] = kaplan_meier_fit
        hazard["count_total"] = count_total
        hazard["count_observed"] = count_observed
        hazard["is_default"] = is_default
        hazard["hazzard_ratio_mean"] = hazzard_ratio_mean
        hazard["hazzard_ratio_lower"] = hazzard_ratio_lower
        hazard["hazzard_ratio_upper"] = hazzard_ratio_upper
        return hazard

    def add_feature_hazard(self, data_frame: pandas.DataFrame, name_feature_hazard: str, include_missing: bool):
        # TODO loop
        # TODO refactor this
        # TODO properly use the fitter without the dead_fraction BS
        # TODO properly use None and nan instead of magic missing attribute
        data_frame_target = data_frame[[self.name_feature_duration, self.name_feature_observation, name_feature_hazard]]
        data_frame_target = data_frame_target[
            data_frame_target[self.name_feature_observation].notna()
        ]  # TODO this is shit

        contains_missing = 0 < data_frame_target[name_feature_hazard].isna().sum()
        if include_missing and contains_missing:
            list_name_value = pandas.unique(data_frame_target[name_feature_hazard])
            if "missing" in list_name_value:
                raise ValueError("feature contains both nan and missing")
            data_frame_target = data_frame_target.fillna("missing")
            list_name_value = sorted(pandas.unique(data_frame_target[name_feature_hazard]))
            list_name_value.remove("missing")
            list_name_value.append("missing")
        else:
            data_frame_target = data_frame_target[data_frame_target[name_feature_hazard].notna()]
            list_name_value = sorted(pandas.unique(data_frame_target[name_feature_hazard]))

        name_value = "all"
        survival_curve_all = ModelNaiveHazard.fit_kaplan_meier(
            data_frame_target, self.name_feature_duration, self.name_feature_observation
        )

        ratio_reference = scipy.interpolate.interp1d(survival_curve_all["domain"], survival_curve_all["mean"])(
            self.time_point
        )

        self.dict_dict_hazard[name_feature_hazard] = {}
        # TODO this next line is problematic, since it it a magic value
        self.dict_dict_hazard[name_feature_hazard]["all"] = ModelNaiveHazard.compute_hazard(
            ratio_reference, survival_curve_all, self.time_point
        )
        for name_value in list_name_value:
            data_frame_hazard = data_frame_target.query(f"(`{name_feature_hazard}` == '{name_value}')")
            survival_curve = ModelNaiveHazard.fit_kaplan_meier(
                data_frame_hazard, self.name_feature_duration, self.name_feature_observation
            )
            self.dict_dict_hazard[name_feature_hazard][name_value] = ModelNaiveHazard.compute_hazard(
                ratio_reference, survival_curve, self.time_point
            )

    def fit(
        self,
        data_frame: pandas.DataFrame,
        name_feature_duration: str,
        name_feature_observation: str,
        list_name_feature_hazard: List[str],
        include_missing: bool = True,
    ) -> None:
        self.name_feature_duration = name_feature_duration
        self.name_feature_observation = name_feature_observation
        self.list_name_feature_hazard = list_name_feature_hazard
        for name_feature in list_name_feature_hazard:
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

    def print(self) -> None:
        for name_feature, dict_hazard in self.dict_dict_hazard.items():
            print(name_feature)
            for name_value, hazard in dict_hazard.items():
                str_value = name_value[:20].ljust(20)
                str_hr = "HR = "
                str_hr += "{:.2f}".format(hazard["hazzard_ratio_mean"])
                str_hr += " (CI = "
                str_hr += "{:.2f}".format(hazard["hazzard_ratio_lower"])
                str_hr += " - "
                str_hr += "{:.2f}".format(hazard["hazzard_ratio_upper"])
                str_hr += ")"
                if hazard["is_default"]:
                    str_hr += " default"
                print(f"  {str_value} {str_hr}")

    def plot(self, data_frame: pandas.DataFrame, name_feature_group: str):
        figure, axes = plt.subplots(figsize=(15, 8), dpi=80)
        list_name_value = pandas.unique(data_frame[name_feature_group])
        for name_value in list_name_value:
            data_frame_target = data_frame[
                [self.name_feature_duration, self.name_feature_observation, name_feature_group]
            ]
            data_frame_target = data_frame_target[data_frame_target[self.name_feature_observation].notna()]
            data_frame_hazard = data_frame_target.query(f"(`{name_feature_group}` == '{name_value}')")

            survival_curve = ModelNaiveHazard.fit_kaplan_meier(
                data_frame_hazard, self.name_feature_duration, self.name_feature_observation
            )
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

    def plot_hazard(self) -> List:
        list_figure = []
        for name_feature_hazard, dict_hazard in self.dict_dict_hazard.items():
            figure, axes = plt.subplots(figsize=(15, 8), dpi=80)
            for name_value, hazard in dict_hazard.items():
                survival_curve = hazard["survival_curve"]
                count_observed = survival_curve["count_observed"]
                count_total = survival_curve["count_total"]
                name_series = f"{name_value} (N={count_observed}/{count_total})"
                if name_value == "all":
                    visualization.plot_survival_curve(axes, survival_curve, name_series, line_style="dashed")
                elif name_value == "missing":
                    visualization.plot_survival_curve(axes, survival_curve, name_series, line_style="dotted")
                else:
                    visualization.plot_survival_curve(axes, survival_curve, name_series)
            axes.legend()
            axes.set_ylabel("survival faction")
            axes.set_label("name_feature_duration")
            axes.set_title(name_feature_hazard)
            list_figure.append(figure)
        return list_figure
