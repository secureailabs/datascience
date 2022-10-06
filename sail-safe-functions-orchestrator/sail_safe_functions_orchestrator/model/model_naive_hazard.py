from typing import Dict, List

import matplotlib.pyplot as plt
import numpy
import pandas
import scipy
from lifelines import KaplanMeierFitter
from sail_safe_functions_orchestrator import preprocessing, visualization
from sail_safe_functions_orchestrator.data_frame_federated import DataFrameFederated
from sail_safe_functions_orchestrator.model.model_base import ModelBase
from sail_safe_functions_orchestrator.model.model_kaplan_meier import ModelKaplanMeier
from sail_safe_functions_test.helper_sail_safe_functions.data_frame_federated_local import DataFrameFederatedLocal


class ModelNaiveHazard(ModelBase):
    # TODO if you are reading this and are asked to refactor this code,
    # be aware that the whole thing is a dumpster fire
    def __init__(self, time_point) -> None:
        super().__init__()
        self.list_name_feature_hazard = []
        self.name_feature_duration = ""
        self.name_feature_observation = ""
        self.dict_dict_hazard = {}
        self.time_point = time_point

    def add_feature_hazard(self, data_frame: DataFrameFederated, name_feature_hazard: str, include_missing: bool):
        # TODO loop
        # TODO refactor this
        # TODO properly use None and nan instead of magic missing attribute
        data_frame_target = preprocessing.select_column(
            data_frame, [self.name_feature_duration, self.name_feature_observation, name_feature_hazard]
        )
        data_frame_target = preprocessing.drop_rows_with_missing_data(
            data_frame_target, [self.name_feature_observation]
        )
        # TODO start probleblamtic section
        data_frame_target = data_frame_target.to_pandas()

        contains_missing = 0 < data_frame_target[name_feature_hazard].isna().sum()
        if include_missing and contains_missing:
            list_name_value = pandas.unique(data_frame_target[name_feature_hazard])
            if "missing" in list_name_value:
                raise ValueError("feature contains both nan and missing")
            data_frame_target = data_frame_target.fillna("missing")
            list_name_value = sorted(pandas.unique(data_frame_target[name_feature_hazard]))
            # Move the missing attribute to the end
            list_name_value.remove("missing")
            list_name_value.append("missing")
        else:
            data_frame_target = data_frame_target[data_frame_target[name_feature_hazard].notna()]
            list_name_value = sorted(pandas.unique(data_frame_target[name_feature_hazard]))

        data_frame_target = DataFrameFederatedLocal.from_data_frame(data_frame_target, 3)

        # TODO end probleblamtic section

        name_value = "all"
        model_kaplan_meier = ModelKaplanMeier()
        model_kaplan_meier.fit(data_frame_target, self.name_feature_duration, self.name_feature_observation)
        survival_curve_all = model_kaplan_meier.get_survival_curve_dict()
        ratio_reference = scipy.interpolate.interp1d(survival_curve_all["domain"], survival_curve_all["mean"])(
            self.time_point
        )

        self.dict_dict_hazard[name_feature_hazard] = {}
        # TODO this next line is problematic, since it it a magic value `all`
        self.dict_dict_hazard[name_feature_hazard]["all"] = model_kaplan_meier.compute_hazard(
            ratio_reference, self.time_point
        )
        for name_value in list_name_value:
            data_frame_hazard = preprocessing.query(data_frame_target, f"(`{name_feature_hazard}` == '{name_value}')")
            model_kaplan_meier = ModelKaplanMeier()
            model_kaplan_meier.fit(data_frame_hazard, self.name_feature_duration, self.name_feature_observation)
            self.dict_dict_hazard[name_feature_hazard][name_value] = model_kaplan_meier.compute_hazard(
                ratio_reference, self.time_point
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

    def predict(self, data_frame_source: DataFrameFederated, name_feature_score: str):
        # TODO problem this is not federated at all
        data_frame = data_frame_source.to_pandas()
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
        return DataFrameFederatedLocal.from_data_frame(data_frame, 3)

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
            axes.set_label(self.name_feature_duration)
            axes.set_title(name_feature_hazard)
            list_figure.append(figure)
        return list_figure
