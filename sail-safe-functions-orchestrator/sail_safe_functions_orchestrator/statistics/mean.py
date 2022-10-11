import numpy
from sail_safe_functions.statistics.mean_aggregate import MeanAggregate
from sail_safe_functions.statistics.mean_precompute import MeanPrecompute
from sail_safe_functions_orchestrator.series_federated import SeriesFederated
from sail_safe_functions_orchestrator.statistics.estimator import Estimator


def mean(sample_0: SeriesFederated):
    """
    Perform federated Mean.
    It takes one federated series, and returns the mean value

    :param sample_0: sample series
    :type sample_0: SeriesFederated
    :return: mean value of federated series
    :rtype: float
    """
    estimator = Mean()
    return estimator.run(sample_0)


class Mean(Estimator):
    def __init__(self) -> None:
        super().__init__(["mean"])

    def run(self, sample_0: SeriesFederated):
        """
        It takes one federated series, and returns the Mean

        :param sample_0: _description_
        :type sample_0: SeriesFederated
        :return: _description_
        :rtype: _type_
        """

        list_list_precompute = []
        for dataset_id in sample_0.list_dataset_id:
            client = sample_0.service_client.get_client(dataset_id)
            reference_series = sample_0.get_reference_series(dataset_id)
            list_list_precompute.append(client.call(MeanPrecompute, reference_series))
        mean_statistic = MeanAggregate.run(list_list_precompute)  # TODO this does not need to get merged
        return mean_statistic

    def run_reference(self, sample_0: SeriesFederated):
        return numpy.mean(sample_0.to_numpy())
