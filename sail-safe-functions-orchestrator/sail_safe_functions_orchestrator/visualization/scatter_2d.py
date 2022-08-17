import matplotlib.pyplot as plt  # TODO replace
import numpy
from sail_safe_functions_orchestrator.series_federated import SeriesFederated


def scatter_2d(sample_0: SeriesFederated, sample_1: SeriesFederated, sample_split: SeriesFederated = None):
    # TODO add plotliy
    # TODO add privacy
    if sample_split is None:
        plt.scatter(sample_0.to_numpy(), sample_1.to_numpy())
    else:
        array_split = sample_split.to_numpy()
        array_unique = numpy.unique(array_split)
        list_unique = []
        for unique in array_unique:
            if 1 < len(sample_0.to_numpy()[array_split == unique]):
                list_unique.append(unique)
                plt.scatter(sample_0.to_numpy()[array_split == unique], sample_1.to_numpy()[array_split == unique])
        plt.legend(list_unique)
    plt.show()
