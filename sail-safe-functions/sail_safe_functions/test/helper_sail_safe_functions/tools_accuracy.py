from typing import List

import numpy
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sail_safe_functions.aggregator.statistics.estimator import Estimator
from sail_safe_functions.aggregator.statistics.estimator_one_sample import EstimatorOneSample
from sail_safe_functions.aggregator.statistics.estimator_two_sample import EstimatorTwoSample
from sail_safe_functions.test.helper_sail_safe_functions.estimator_one_sample_reference import (
    EstimatorOneSampleReference,
)
from sail_safe_functions.test.helper_sail_safe_functions.estimator_two_sample_reference import (
    EstimatorTwoSampleReference,
)
from sail_safe_functions.test.helper_sail_safe_functions.generator_one_sample_float import GeneratorOneSampleFloat
from sail_safe_functions.test.helper_sail_safe_functions.generator_two_sample_float import GeneratorTwoSampleFloat
from sail_safe_functions.test.helper_sail_safe_functions.tools_privacy import compute_single_knockout_privacy_measure
from scipy import interpolate


def evaluate_accuracy(
    estimator: EstimatorOneSample,
    generator: GeneratorOneSampleFloat,
    list_sample_size: List[int],
    count_run_bias_variance: int,
    count_run_privacy: int,
):
    estimator_reference = EstimatorOneSampleReference(estimator)
    # accuracy
    # bias
    count_estimate = len(estimator.list_estimate_name)
    report = {}
    report["list_size_sample"] = list_sample_size
    report["list_estimate_name"] = estimator.list_estimate_name
    report["count_run_bias_variance"] = count_run_bias_variance
    report["count_run_privacy"] = count_run_privacy
    report["dict_estimate"] = {}
    for name_estimate in estimator.list_estimate_name:
        report["dict_estimate"][name_estimate] = {}
        report["dict_estimate"][name_estimate]["list_error_mean"] = []
        report["dict_estimate"][name_estimate]["list_variance"] = []
        report["dict_estimate"][name_estimate]["list_privacy_estimator_mean"] = []
        report["dict_estimate"][name_estimate]["list_privacy_reference_mean"] = []
    for sample_size in list_sample_size:
        array_error = numpy.zeros((count_run_bias_variance, count_estimate))
        for index_run in range(count_run_bias_variance):
            sample = generator.generate(sample_size)
            array_error[index_run, :] = numpy.array(estimator_reference.run(sample)) - numpy.array(
                estimator.run(sample)
            )
        for i, name_estimate in enumerate(estimator.list_estimate_name):
            error_mean = numpy.mean(array_error[:, i])
            variance = numpy.var(array_error[:, i], ddof=1)
            report["dict_estimate"][name_estimate]["list_error_mean"].append(error_mean)
            report["dict_estimate"][name_estimate]["list_variance"].append(variance)

    for sample_size in list_sample_size:
        array_estimator = numpy.zeros((count_run_privacy, count_estimate))
        array_reference = numpy.zeros((count_run_privacy, count_estimate))
        for index_run in range(count_run_privacy):
            sample = generator.generate(sample_size)
            array_estimator[index_run, :] = compute_single_knockout_privacy_measure(estimator, sample)
            array_reference[index_run, :] = compute_single_knockout_privacy_measure(
                estimator_reference, sample
            )  # TODO set reference

        for i, name_estimate in enumerate(estimator.list_estimate_name):
            privacy_estimator = numpy.mean(array_estimator[:, i])
            privacy_reference = numpy.mean(array_reference[:, i])
            report["dict_estimate"][name_estimate]["list_privacy_estimator_mean"].append(privacy_estimator)
            report["dict_estimate"][name_estimate]["list_privacy_reference_mean"].append(privacy_reference)

    return report


def plot_estimator_summary_go(report, name_estimate):
    # for the executive summary we compute our stats at the sample_size=10 level and normalize them according to the underlining distribution (sd=1)
    accuracy_10 = abs(
        interpolate.interp1d(report["list_size_sample"], report["dict_estimate"][name_estimate]["list_error_mean"])(10)
    )
    efficiency_10 = numpy.sqrt(
        interpolate.interp1d(report["list_size_sample"], report["dict_estimate"][name_estimate]["list_variance"])(10)
    )
    privacy_10_e = interpolate.interp1d(
        report["list_size_sample"], report["dict_estimate"][name_estimate]["list_privacy_estimator_mean"]
    )(10)
    privacy_10_r = interpolate.interp1d(
        report["list_size_sample"], report["dict_estimate"][name_estimate]["list_privacy_reference_mean"]
    )(10)

    # normalize measures
    # note that test distrbution are asumeted to 1=sd #TODO check this

    # for accuracy 1 is no bias, 0 is 10^0.5 sd bias (50% outside side the 95% range )
    # TODO relate this to cramer rao
    accuracy = 1 - (accuracy_10 * numpy.sqrt(10))

    # for efficenty 1 is no variance, and 0 is 10^0.5 sd bias (spread larger than that of distribution)
    # TODO make this relate to cramer rao lower bound
    efficiency = 1 - (efficiency_10 * numpy.sqrt(10))

    # for privacy 1 is no knockout difference, and 0 is 2 time reference difference
    # TODO relate this to kl divergence
    privacy = 1 - (privacy_10_e / (privacy_10_r * 2))

    # clamp measures
    accuracy = max(0, min(1, accuracy))
    efficiency = max(0, min(1, efficiency))
    privacy = max(0, min(1, privacy))

    return go.Scatterpolar(
        name=name_estimate, r=[accuracy, efficiency, privacy], theta=["accuracy", "effciency", "privacy"], fill="toself"
    )


def plot_estimator_comparrison(list_tuple_report):
    list_go = []
    for report, name_estimate in list_tuple_report:
        list_go.append(plot_estimator_summary_go(report, name_estimate))

    fig = go.Figure(data=list_go)

    fig.update_layout(
        height=400,
        width=400,
        title_text=f"Comparison",
        polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
        showlegend=True,
    )
    fig.show()


def plot_report_estimator(title, report):

    for name_estimate in report["list_estimate_name"]:
        list_subplot_title = []
        list_subplot_title.append(f'"{name_estimate}" bias')
        list_subplot_title.append(f'"{name_estimate}" efficiency / quality')
        list_subplot_title.append(f'"{name_estimate}" suffcientcy / privacy')

        fig = make_subplots(rows=1, cols=3, subplot_titles=list_subplot_title)

        go_bias = go.Scatter(
            x=report["list_size_sample"],
            y=report["dict_estimate"][name_estimate]["list_error_mean"],
            line=dict(color="#0000ff"),
        )
        go_sd = go.Scatter(
            x=report["list_size_sample"],
            y=report["dict_estimate"][name_estimate]["list_variance"],
            line=dict(color="#0000ff"),
        )
        go_privacy_estimator = go.Scatter(
            x=report["list_size_sample"],
            y=report["dict_estimate"][name_estimate]["list_privacy_estimator_mean"],
            line=dict(color="#0000ff"),
        )

        go_privacy_reference = go.Scatter(
            x=report["list_size_sample"],
            y=report["dict_estimate"][name_estimate]["list_privacy_reference_mean"],
            line=dict(color="#ff0000"),
        )

        fig.add_trace(go_bias, row=1, col=1)
        fig.add_trace(go_sd, row=1, col=2)
        fig.add_trace(go_privacy_estimator, row=1, col=3)
        fig.add_trace(go_privacy_reference, row=1, col=3)

        fig["layout"]["xaxis"]["title"] = "sample size"
        fig["layout"][f"xaxis2"]["title"] = "sample size"
        fig["layout"][f"xaxis3"]["title"] = "sample size"

        fig.update_layout(height=350, width=800, title_text="Quality report for " + title, showlegend=False)
        fig.show()

        fig = go.Figure(data=plot_estimator_summary_go(report, name_estimate))

        fig.update_layout(
            height=400,
            width=400,
            title_text=f"Summary for {name_estimate}",
            polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
            showlegend=False,
        )
        fig.show()


def plot_report_power(report_power: dict, title: str):
    list_subplot_titles = []
    for sample_size in report_power["list_sample_size"]:
        list_subplot_titles.append(f"N={sample_size}")

    fig = make_subplots(
        rows=1, cols=len(report_power["list_sample_size"]), shared_yaxes=True, subplot_titles=list_subplot_titles
    )

    for i, sample_size in enumerate(report_power["list_sample_size"]):
        go_bias = go.Scatter(
            x=report_power["list_effect_size"], y=report_power["list_list_fraction_hit"][i], line=dict(color="#0000ff")
        )
        fig.add_trace(go_bias, row=1, col=i + 1)

    fig["layout"]["yaxis"]["title"] = "statistical power"
    fig["layout"]["xaxis"]["title"] = "effect size"
    for i in range(len(report_power["list_sample_size"]) - 1):
        fig["layout"][f"xaxis{i+2}"]["title"] = "effect size"

    fig.update_layout(height=350, width=1200, title_text="Quality report for " + title, showlegend=False)
    fig.show()


def plot_list_report_power(list_report_power: List[dict]):
    list_subplot_titles = []
    list_sample_size = list_report_power[0]["list_sample_size"]
    for sample_size in list_sample_size:
        list_subplot_titles.append(f"N={sample_size}")

    fig = make_subplots(rows=1, cols=len(list_subplot_titles), shared_yaxes=True, subplot_titles=list_subplot_titles)

    for i, sample_size in enumerate(list_sample_size):
        for report_power in list_report_power:
            go_power = go.Scatter(
                x=report_power["list_effect_size"],
                y=report_power["list_list_fraction_hit"][i],
                line=dict(color="#0000ff"),
            )
            fig.add_trace(go_power, row=1, col=i + 1)

    fig["layout"]["yaxis"]["title"] = "statistical power"
    fig["layout"]["xaxis"]["title"] = "effect size"
    for i in range(len(report_power["list_sample_size"]) - 1):
        fig["layout"][f"xaxis{i+2}"]["title"] = "effect size"

    fig.update_layout(height=350, width=1200, showlegend=False)
    fig.show()


def experiment_bias_variance_two_sample(
    estimator: EstimatorTwoSample,
    generator: GeneratorTwoSampleFloat,
    sample_size: int,
    effect_size: float,
    is_paired: bool,
    significance: float,
    run_count: int,
    target_estimate_name: str,
) -> dict:

    experiment = {}
    experiment["parameter"] = {}
    experiment["parameter"]["estimator_name"] = estimator.estimator_name + " - " + target_estimate_name
    experiment["parameter"]["generator_name"] = generator.name
    experiment["parameter"]["sample_size"] = sample_size
    experiment["parameter"]["effect_size"] = effect_size
    experiment["parameter"]["significance"] = significance
    experiment["parameter"]["run_count"] = run_count
    experiment["parameter"]["target_estimate_name"] = target_estimate_name
    # TODO check if experiment is cached

    estimator_reference = EstimatorTwoSampleReference(estimator)

    estimate_index = estimator.get_estimate_index(target_estimate_name)
    list_estimate: List[float] = []
    list_estimate_reference: List[float] = []

    for _ in range(run_count):
        sample_0, sample_1 = generator.generate(sample_size, effect_size, is_paired)
        tuple_estimate = estimator.run(sample_0, sample_1)
        tuple_estimate_reference = estimator_reference.run(sample_0, sample_1)
        list_estimate.append(tuple_estimate[estimate_index])
        list_estimate_reference.append(tuple_estimate_reference[estimate_index])

    array_error = numpy.array(list_estimate, dtype=numpy.float64) - numpy.array(
        list_estimate_reference, dtype=numpy.float64
    )
    error_bias = numpy.mean(array_error)
    error_varriance = numpy.var(array_error)

    experiment["result"] = {}
    experiment["result"]["list_estimate"] = list_estimate
    experiment["result"]["list_estimate_reference"] = list_estimate_reference
    experiment["result"]["list_estimate_error"] = array_error.tolist()
    experiment["result"]["error_bias"] = error_bias
    experiment["result"]["error_varriance"] = error_varriance
    return experiment


def experiment_power(
    estimator: EstimatorTwoSample,
    generator: GeneratorTwoSampleFloat,
    sample_size: int,
    effect_size: float,
    is_paired: bool,
    significance: float,
    run_count: int,
) -> dict:
    hit_count = 0
    for _ in range(run_count):
        sample_0, sample_1 = generator.generate(sample_size, effect_size, is_paired)
        _, p_value = estimator.run(sample_0, sample_1)
        if p_value < significance:
            hit_count += 1
    fraction_hit = hit_count / run_count
    experiment = {}
    experiment["parameter"] = {}
    experiment["parameter"]["estimator_name"] = estimator.estimator_name
    experiment["parameter"]["generator_name"] = generator.name
    experiment["parameter"]["sample_size"] = sample_size
    experiment["parameter"]["effect_size"] = effect_size
    experiment["parameter"]["significance"] = significance
    experiment["parameter"]["run_count"] = run_count

    experiment["result"] = {}
    experiment["result"]["statistical_power"] = fraction_hit
    return experiment


def plot_experiment_power(list_sample_size, list_list_list_experiment: List[List[List[dict]]]):
    list_subplot_titles = []
    for sample_size in list_sample_size:
        list_subplot_titles.append(f"N={sample_size}")

    fig = make_subplots(rows=1, cols=len(list_sample_size), shared_yaxes=True, subplot_titles=list_subplot_titles)
    dict_line = {}
    for index_col, list_list_experiment in enumerate(list_list_list_experiment):
        show_legend = index_col == len(list_sample_size) - 1
        for index_estimator, list_experiment in enumerate(list_list_experiment):

            add_trace_experiment(
                fig,
                1,
                index_col + 1,
                "effect_size",
                "statistical_power",
                "estimator_name",
                show_legend,
                dict_line,
                list_experiment,
            )

    fig["layout"]["xaxis"]["title"] = "effect size"
    for i in range(len(list_sample_size) - 1):
        fig["layout"][f"xaxis{i+2}"]["title"] = "effect size"
    fig["layout"]["yaxis"]["title"] = "statistical power"
    fig.update_layout(height=350, width=1200, showlegend=True)
    fig.show()


def plot_experiment_bias_variance_two_sample_hist(list_experiment: List[dict]):
    list_subplot_titles = []
    list_sample_size = []
    for experiment in list_experiment:
        list_sample_size.append(experiment["parameter"]["sample_size"])
    for sample_size in list_sample_size:
        list_subplot_titles.append(f"N={sample_size}")

    fig = make_subplots(rows=1, cols=len(list_sample_size), shared_yaxes=True, subplot_titles=list_subplot_titles)
    dict_line = {}
    for index_col, experiment in enumerate(list_experiment):
        show_legend = index_col == len(list_sample_size) - 1

        add_trace_experiment_hist(
            fig,
            1,
            index_col + 1,
            "list_estimate_error",
            "estimator_name",
            show_legend,
            dict_line,
            experiment,
        )

    fig["layout"]["xaxis"]["title"] = "error"
    for i in range(len(list_sample_size) - 1):
        fig["layout"][f"xaxis{i+2}"]["title"] = "error"
    fig["layout"]["yaxis"]["title"] = "frequency"
    fig.update_layout(height=350, width=1200, showlegend=True)
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
    if name not in dict_line:
        line = dict(color=px.colors.qualitative.Plotly[len(dict_line)])
        dict_line[name] = line

    line = dict_line[name]
    go_power = go.Scatter(
        x=list_x_sorted, y=list_y_sorted, name=name, legendgroup=name, showlegend=show_legend, line=line
    )
    fig.add_trace(go_power, row=index_row, col=index_col)


def add_trace_experiment_hist(
    fig,
    index_row: int,
    index_col: int,
    attribute_x: str,
    attribute_name: str,
    show_legend: bool,
    dict_line: dict,
    experiment: dict,
):
    name = experiment["parameter"][attribute_name]
    # gather data
    list_x = experiment["result"][attribute_x]
    if name not in dict_line:
        line = dict(color=px.colors.qualitative.Plotly[len(dict_line)])
        dict_line[name] = line

    line = dict_line[name]
    go_hist = go.Histogram(
        histfunc="count",
        x=list_x,
        name=name,
        legendgroup=name,
        showlegend=show_legend,
        #        marker=px.colors.qualitative.Plotly
    )

    fig.add_trace(go_hist, row=index_row, col=index_col)


# def plot_line_grid(
#     list_experiment,
#     field_subplot_row: str,
#     field_subplot_col: str,
#     field_subplot_stack: str,
#     name_data_x: str,
#     name_data_y: str,
# ):
#     dict_row = {}
#     list_value_subplot_row = []
#     list_value_subplot_col = []
#     list_value_subplot_stack = []
#     for experiment in list_experiment:
#         value_row = experiment[field_subplot_row]
#         value_col = experiment[field_subplot_col]
#         if value_row not in dict_row:
#             dict_row[value_row] = {}

#         if value_col not in dict_row[value_row]:
#             dict_row[value_row][value_row] = []
#         dict_row[value_row][value_row].append(experiment)
#     list_field_subplot_row
#     fig = make_subplots(rows=1, cols=len(list_subplot_titles), shared_yaxes=True, subplot_titles=list_subplot_titles)


def create_report_power(
    estimator_test: Estimator,
    generator: GeneratorTwoSampleFloat,
    list_sample_size: List[int],
    list_effect_size: List[float],
    is_paired: bool = False,
    significance: float = 0.05,
    run_count: int = 100,
):
    count_hit = 0
    report = {}
    report["list_sample_size"] = list_sample_size
    report["list_effect_size"] = list_effect_size
    report["list_list_fraction_hit"] = []
    for sample_size in list_sample_size:
        list_fraction_hit = []
        for effect_size in list_effect_size:
            hit_count = 0
            for _ in range(run_count):
                sample_0, sample_1 = generator.generate(sample_size, effect_size, is_paired)
                t, p = estimator_test.run(sample_0, sample_1)
                if p < significance:
                    hit_count += 1
            list_fraction_hit.append(hit_count / run_count)

        report["list_list_fraction_hit"].append(list_fraction_hit)
    return report
