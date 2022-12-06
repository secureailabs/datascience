import numpy
import plotly.figure_factory as ff
from sail_safe_functions.visualization.kernel_density_estimation_aggregate import \
    KernelDensityEstimationAggregate
from sail_safe_functions.visualization.kernel_density_estimation_precompute import \
    KernelDensityEstimationPrecompute
from sail_safe_functions_orchestrator.series_federated import SeriesFederated


def kernel_density_estimation(sample_0: SeriesFederated, bin_size: float):
    """
    Performs the federated kernel density estimation.
    It take on federated series and bin count. Returns the kde plot.
    -----------
        :param sample_0: The first sample of data
        :type sample_0: SeriesFederated
        :param bin_size: The second sample of data
        :type bin_size: float
        :return: pyplot figure valuie
        :rtype: pyplot object

    """

    return KernelDensityEstimation.run(sample_0, bin_size)


class KernelDensityEstimation:
    """
    Performs the federated kernel density estimation.

    """

    @staticmethod
    def run(sample_0: SeriesFederated, bin_size: float):
        list_list_precompute = []
        for dataset_id in sample_0.list_dataset_id:
            client = sample_0.service_client.get_client(dataset_id)
            list_list_precompute.append(
                client.call(
                    KernelDensityEstimationPrecompute,
                    sample_0.dict_reference_series[dataset_id],
                )
            )
        kde_value = KernelDensityEstimationAggregate.run(list_list_precompute)
        list_kde_value = [kde_value]
        list_group_label = [sample_0.series_name]
        fig = ff.create_distplot(list_kde_value, list_group_label, bin_size)
        fig_dict = fig.to_dict()
        # TODO sanitizing plotly, we could do better
        for i, data_dict in enumerate(fig_dict["data"]):
            if "x" in data_dict:
                if isinstance(data_dict["x"], numpy.ndarray):
                    fig_dict["data"][i]["x"] = list(data_dict["x"])
                    print("replace x")
            if "y" in data_dict:
                if isinstance(data_dict["y"], numpy.ndarray):
                    fig_dict["data"][i]["y"] = list(data_dict["y"])
                    print("replace y")
        return fig_dict
