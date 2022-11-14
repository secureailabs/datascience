import plotly.figure_factory as ff
from sail_safe_functions.visualization.KernelDensityEstimation_aggregate import KernelDensityEstimationAggregate
from sail_safe_functions.visualization.KernelDensityEstimation_precompute import KernelDensityEstimationPrecompute
from sail_safe_functions_orchestrator.series import Series


class KernelDensityEstimation_class:
    """
    Performs the federated kernel density estimation.

    """

    @staticmethod
    def KernelDensityEstimation(sample_0: Series, group_labels: str, bin_size: float):
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
        fig = ff.create_distplot(kde_value, group_labels, bin_size)
        return fig

    @staticmethod
    def run(sample_0: Series, group_labels: str, bin_size: float):
        return KernelDensityEstimation_class.KernelDensityEstimation(sample_0, group_labels, bin_size)
