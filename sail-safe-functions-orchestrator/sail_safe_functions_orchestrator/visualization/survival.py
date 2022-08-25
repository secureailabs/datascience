import matplotlib.pyplot as plt  # TODO replace
import numpy
import pandas
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


def survival_plot(data_frame: pandas.DataFrame):
    count_total = data_frame["vital_status"].notna().count()
    array_death_years_to = (
        data_frame["death_days_to"][data_frame["death_days_to"].notna()].astype(float).to_numpy() / 365.25
    )

    array_surival_time = numpy.sort(array_death_years_to)
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


def survival_gene(data_frame: pandas.DataFrame, name_gene: str, x_label: str, title: str):
    fig, ax = plt.subplots(figsize=(15, 8), dpi=80)
    name_feature = "count_mutation_" + name_gene
    data_frame_genetics = data_frame[data_frame[name_feature].notna()]
    survival_plot(data_frame_genetics[data_frame_genetics[name_feature] == 0])
    survival_plot(data_frame_genetics[data_frame_genetics[name_feature] != 0])
    list_legend = ["Survival without mutation in " + name_gene, "Survival with at least one mutation in " + name_gene]
    plt.ylabel("survival faction")
    plt.xlabel(x_label)
    plt.title(title)
    plt.legend(list_legend)
    plt.show()
    return fig


def survival_new(
    data_frame: DataFrameFederated,
    name_feature_survival_time: str,
    name_feature_split: str = None,
):
    # TODO add plotliy
    # TODO add privacy
    domain_min, domain_max = statistics.min_max(sample_0)
    array_domain = numpy.linspace(domain_min, domain_max, 100)
    if sample_split is None:
        array_value = kde(array_domain, sample_0.to_numpy(), kernel_standard_deviation)
        fig, ax = plt.subplots(figsize=(20, 12), dpi=80)
        ax.plot(array_domain, array_value)
        ax.fill_between(array_domain, numpy.zeros(len(array_domain)), array_value, alpha=0.2)
    else:
        array_split = sample_split.to_numpy()
        array_unique = numpy.unique(array_split)
        fig, ax = plt.subplots(figsize=(20, 12), dpi=80)
        list_unique = []
        for unique in array_unique:
            if 1 < len(sample_0.to_numpy()[array_split == unique]):
                array_value = kde(array_domain, sample_0.to_numpy()[array_split == unique], kernel_standard_deviation)
                ax.plot(array_domain, array_value)
                list_unique.append(unique)
        for unique in array_unique:
            if 1 < len(sample_0.to_numpy()[array_split == unique]):
                array_value = kde(array_domain, sample_0.to_numpy()[array_split == unique], kernel_standard_deviation)
                ax.fill_between(array_domain, numpy.zeros(len(array_domain)), array_value, alpha=0.2)
            # plt.scatter(sample_0.to_numpy()[array_split == unique], sample_1.to_numpy()[array_split == unique])
        plt.legend(list_unique)
    plt.ylabel("likelihood")
    plt.xlabel(name_feature_data)
    plt.show()
    return fig
