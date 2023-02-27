from typing import List

import numpy
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sail_safe_functions.aggregator import statistics
from sail_safe_functions.aggregator.series_federated import SeriesFederated
from sail_safe_functions.aggregator.statistics.estimator_one_sample import EstimatorOneSample
from sail_safe_functions.test.helper_sail_safe_functions.tools_data_test import (
    series_drop_by_index,
    series_split_random,
)


def compute_single_knockout_privacy_measure(
    estimator: EstimatorOneSample,
    series_0: SeriesFederated,
):
    estimate_full = numpy.array(estimator.run(series_0))
    error_abs_max = numpy.zeros(estimate_full.shape)
    sample_size = statistics.count((series_0))
    for i in range(sample_size):
        series_0_single_knockout = series_drop_by_index(series_0, i)

        estimate_single_knockout = numpy.array(estimator.run(series_0_single_knockout))
        error_abs = numpy.abs(estimate_full - estimate_single_knockout)
        error_abs_max = numpy.maximum(error_abs_max, error_abs)
    return error_abs_max


def experiment_privacy_one_sample_dma(
    estimator: EstimatorOneSample,
    series_0: SeriesFederated,
    extract_fraction: float,
    run_count: int,
) -> dict:
    # perfroms a number of automated Divergence Membership Attacks and sees how many pass
    # NOTE divergence is abs error

    if extract_fraction <= 0 or 1 < extract_fraction:
        raise Exception("extract fraction must be between 0 and 1")

    experiment = {}
    experiment["parameter"] = {}
    experiment["parameter"]["estimator_name"] = estimator.estimator_name
    experiment["parameter"]["series_name"] = series_0.series_name
    experiment["parameter"]["extract_fraction"] = extract_fraction
    experiment["parameter"]["run_count"] = run_count

    # TODO series should be of equal size
    size = statistics.count(series_0)
    size_series_a = size // 2
    size_series_b = size // 2
    size_series_e = int(size_series_a * extract_fraction)
    if size_series_e <= 0:
        size_series_e = 1

    break_count = 0
    for i in range(run_count):
        series_a, series_b = series_split_random(series_0, size_series_b)

        series_e, _ = series_split_random(series_a, size_series_e)
        if 1 < len(estimator.list_estimate_name):
            estimate_a = estimator.run(series_a)[0]
            estimate_b = estimator.run(series_b)[0]
            estimate_e = estimator.run(series_e)[0]
        else:
            estimate_a = estimator.run(series_a)
            estimate_b = estimator.run(series_b)
            estimate_e = estimator.run(series_e)
        # todo allow other divergence
        divergence_a = numpy.abs(estimate_a - estimate_e)
        divergence_b = numpy.abs(estimate_b - estimate_e)
        if divergence_a < divergence_b:
            break_count += 1

    fraction_hit = float(break_count) / float(run_count)
    experiment["result"] = {}
    experiment["result"]["fraction_hit"] = fraction_hit
    return experiment


def plot_experiment_privacy_one_sample_dma(list_list_experiment, *, do_show=True):
    xaxis = "extract_fraction"
    yaxis = "fraction_hit"
    trace_axis = "estimator_name"
    list_split_rows = []
    list_split_cols = []
    list_split_trace = []

    list_subplot_titles = ["boem"]
    fig = make_subplots(rows=1, cols=1, shared_yaxes=True, subplot_titles=list_subplot_titles)
    dict_line = {}
    for i_trace, list_experiment in enumerate(list_list_experiment):
        add_trace_experiment(
            fig,
            1,
            1,
            xaxis,
            yaxis,
            trace_axis,
            True,
            dict_line,
            list_experiment,
        )
    fig["layout"]["xaxis"]["title"] = xaxis
    for i in range(1 - 1):
        fig["layout"][f"xaxis{i+2}"]["title"] = xaxis
    fig["layout"]["yaxis"]["title"] = yaxis
    fig.update_layout(height=350, width=1200, showlegend=True)
    if do_show:
        fig.show()


def add_trace_experiment(
    fig,
    index_row: int,
    index_col: int,
    attribute_x: str,
    attribute_y: str,
    attribute_name: str,
    show_legend: bool,
    dict_line: dict,
    list_experiment: List[dict],
):

    name = list_experiment[0]["parameter"][attribute_name]
    # gather data
    list_x = []
    list_y = []
    for experiment in list_experiment:
        list_x.append(experiment["parameter"][attribute_x])
        list_y.append(experiment["result"][attribute_y])
    # sort
    list_x_sorted = [x for x, y in sorted(zip(list_x, list_y), key=lambda pair: pair[0])]
    list_y_sorted = [y for x, y in sorted(zip(list_x, list_y), key=lambda pair: pair[0])]
    # plot
    # go_power = go.Scatter(
    #     x=list_x_sorted,
    #     y=list_y_sorted,
    #     name=name,
    #     line=dict(color="#0000ff"),
    # )
    if name not in dict_line:
        line = dict(color=px.colors.qualitative.Plotly[len(dict_line)])
        dict_line[name] = line

    line = dict_line[name]
    go_power = go.Scatter(
        x=list_x_sorted, y=list_y_sorted, name=name, legendgroup=name, showlegend=show_legend, line=line
    )
    fig.add_trace(go_power, row=index_row, col=index_col)
