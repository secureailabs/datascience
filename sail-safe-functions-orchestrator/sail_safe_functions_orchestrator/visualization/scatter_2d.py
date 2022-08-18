import matplotlib.pyplot as plt  # TODO replace
import numpy
from sail_safe_functions_orchestrator.data_frame_federated import DataFrameFederated
from sail_safe_functions_orchestrator.series_federated import SeriesFederated


def scatter_2d(
    data_frame: DataFrameFederated,
    name_feature_x: str,
    name_feature_y: str,
    sample_split: SeriesFederated = None,
):
    # TODO add plotliy
    # TODO add privacy
    sample_x = data_frame[name_feature_x]
    sample_y = data_frame[name_feature_y]
    fig = plt.figure()
    if sample_split is None:
        plt.scatter(sample_x.to_numpy(), sample_y.to_numpy())
    else:
        array_split = sample_split.to_numpy()
        array_unique = numpy.unique(array_split)
        list_unique = []
        for unique in array_unique:
            if 1 < len(sample_x.to_numpy()[array_split == unique]):
                list_unique.append(unique)
                plt.scatter(sample_x.to_numpy()[array_split == unique], sample_y.to_numpy()[array_split == unique])
        plt.legend(list_unique)
    plt.xlabel(name_feature_x)
    plt.ylabel(name_feature_y)
    plt.show()
    return fig
