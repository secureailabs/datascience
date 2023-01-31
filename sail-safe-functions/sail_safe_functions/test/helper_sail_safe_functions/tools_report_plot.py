from typing import List

import numpy
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sail_safe_functions.aggregator.statistics.estimator import Estimator
from sail_safe_functions.test.helper_sail_safe_functions.estimator_one_sample_reference import (
    EstimatorOneSampleReference,
)
from sail_safe_functions.test.helper_sail_safe_functions.generator_one_sample_float import GeneratorOneSampleFloat
from sail_safe_functions.test.helper_sail_safe_functions.generator_two_sample_float import GeneratorTwoSampleFloat
from sail_safe_functions.test.helper_sail_safe_functions.tools_privacy import compute_single_knockout_privacy_measure
from scipy import interpolate


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
