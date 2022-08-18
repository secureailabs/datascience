import matplotlib.pyplot as plt  # TODO replace
import numpy
import scipy
from sail_safe_functions_orchestrator import statistics
from sail_safe_functions_orchestrator.data_frame_federated import DataFrameFederated
from sail_safe_functions_orchestrator.series_federated import SeriesFederated
from sklearn.neighbors import KernelDensity


def kde(array_domain: numpy.ndarray, array_samples: numpy.ndarray, kernel_standard_deviation: float):
    # estimator = KernelDensity(kernel="gaussian", bandwidth=kernel_standard_deviation)
    # estimator.fit(array_samples)
    # return estimator.score_samples(array_domain)

    # TODO make this better using the fast kexxu code
    density = scipy.stats.gaussian_kde(array_samples)
    return density(array_domain)


def kde_1d(
    data_frame: DataFrameFederated,
    name_feature_data: str,
    sample_split: SeriesFederated = None,  # TODO make this part of the dataframe
    kernel_standard_deviation: float = 0.1,
):
    sample_0 = data_frame[name_feature_data]
    # TODO add plotly
    # TODO add privacy
    fig = plt.figure()
    domain_min, domain_max = statistics.min_max(sample_0)
    array_domain = numpy.linspace(domain_min, domain_max, 100)
    if sample_split is None:
        array_value = kde(array_domain, sample_0.to_numpy(), kernel_standard_deviation)
        fig, ax = plt.subplots()
        ax.plot(array_domain, array_value)
        ax.fill_between(array_domain, numpy.zeros(len(array_domain)), array_value, alpha=0.2)
    else:
        array_split = sample_split.to_numpy()
        array_unique = numpy.unique(array_split)
        fig, ax = plt.subplots()
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
