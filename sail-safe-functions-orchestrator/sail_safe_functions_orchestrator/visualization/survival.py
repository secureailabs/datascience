from typing import Dict

import matplotlib.pyplot as plt  # TODO replace
import numpy
import pandas
from matplotlib.axes import Axes
from sail_safe_functions_orchestrator.data_frame_federated import DataFrameFederated
from sail_safe_functions_orchestrator.series_federated import SeriesFederated


def survival(count_total: float, array_surival_time: numpy.ndarray, x_label: str, add_model_fit=False):
    fig, ax = plt.subplots(figsize=(15, 8), dpi=80)
    array_surival_time = numpy.sort(array_surival_time)
    fraction = 1 / count_total
    list_domain = [0.0]
    list_value = [1.0]

    for domain in array_surival_time:
        value_current = list_value[-1]
        list_domain.append(domain)
        list_value.append(value_current)
        value_current -= fraction
        list_domain.append(domain)
        list_value.append(value_current)

    # do a more refined curve fit
    # https://stackoverflow.com/questions/3433486/how-to-do-exponential-and-logarithmic-curve-fitting-in-python-i-found-only-poly

    plt.plot(list_domain, list_value)
    plt.ylabel("likelihood")
    plt.xlabel(x_label)
    plt.show()
    return fig


def survival_plot(data_frame: pandas.DataFrame, name_feature_survival, name_feature_observed):
    count_total = data_frame[name_feature_observed].notna().count()
    array_survival = (
        data_frame[name_feature_survival][data_frame[name_feature_survival].notna()].astype(float).to_numpy()
    )

    array_surival_time = numpy.sort(array_survival)
    fraction = 1 / count_total
    list_domain = [0.0]
    list_value = [1.0]

    for domain in array_surival_time:
        value_current = list_value[-1]
        list_domain.append(domain)
        list_value.append(value_current)
        value_current -= fraction
        list_domain.append(domain)
        list_value.append(value_current)
    plt.plot(list_domain, list_value)


def survival_feature(
    data_frame: pandas.DataFrame,
    name_feature_survival: str,
    name_feature_observation: str,
    label_survival: str,
    title: str,
    dict_query: Dict[str, str],
):
    fig, ax = plt.subplots(figsize=(15, 8), dpi=80)
    list_legend = []
    for name_query, query in dict_query.items():
        data_frame_query = data_frame.query(query)
        count_total = data_frame_query[name_feature_observation].notna().count()
        survival_plot(data_frame_query, name_feature_survival, name_feature_observation)
        list_legend.append(name_query + f"(N={count_total})")
    plt.ylabel("survival faction")
    plt.xlabel(label_survival)
    plt.title(title)
    plt.legend(list_legend)
    plt.show()
    return fig


def survival_gene(
    data_frame: pandas.DataFrame,
    name_feature_survival: str,
    name_feature_observation: str,
    label_survival: str,
    title: str,
    name_gene: str,
):
    name_feature_gene = "has_mutation_" + name_gene
    data_frame = data_frame[data_frame[name_feature_gene].notna()]
    data_frame = data_frame[data_frame[name_feature_observation].notna()]
    dict_query = {}
    dict_query["Survival without mutation in " + name_gene] = "(`" + name_feature_gene + "` == 0)"
    dict_query["Survival with at least one mutation in " + name_gene] = "(`" + name_feature_gene + "` != 0)"
    return survival_query(
        data_frame, name_feature_survival, name_feature_observation, label_survival, title, dict_query
    )


def survival_query(
    data_frame: pandas.DataFrame,
    name_feature_survival: str,
    name_feature_observation: str,
    label_survival: str,
    title: str,
    dict_query: Dict[str, str],
):
    fig, ax = plt.subplots(figsize=(15, 8), dpi=80)
    list_legend = []
    for name_query, query in dict_query.items():
        data_frame_query = data_frame.query(query)
        count_total = data_frame_query[name_feature_observation].notna().count()
        survival_plot(data_frame_query, name_feature_survival, name_feature_observation)
        list_legend.append(name_query + f"(N={count_total})")
    plt.ylabel("survival faction")
    plt.xlabel(label_survival)
    plt.title(title)
    plt.legend(list_legend)
    plt.show()
    return fig


def plot_survival_curve(
    ax: Axes,
    survival_curve: Dict,
    label: str,
    *,
    line_style: str = "solid",
):
    domain = survival_curve["domain"]
    mean = survival_curve["mean"]
    lower = survival_curve["lower"]
    upper = survival_curve["upper"]

    domain_plot = [0.0]
    mean_plot = [1.0]
    lower_plot = [1.0]
    upper_plot = [1.0]
    for i in range(1, len(domain)):
        domain_plot.append(domain[i])
        mean_plot.append(mean[i - 1])
        lower_plot.append(lower[i - 1])
        upper_plot.append(upper[i - 1])
        domain_plot.append(domain[i])
        mean_plot.append(mean[i])
        lower_plot.append(lower[i])
        upper_plot.append(upper[i])
    ax.plot(domain_plot, mean_plot, label=label, linestyle=line_style)
    ax.fill_between(domain_plot, lower_plot, upper_plot, alpha=0.2)


def plot_survival_confidence(
    ax: Axes,
    domain: numpy.ndarray,
    mean: numpy.ndarray,
    lower: numpy.ndarray,
    upper: numpy.ndarray,
    label: str,
    *,
    line_style: str = "solid",
):
    ax.plot(domain, mean, label=label, linestyle=line_style)
    ax.fill_between(domain, lower, upper, alpha=0.2)
