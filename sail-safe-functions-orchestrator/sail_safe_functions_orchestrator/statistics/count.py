import numpy
from sail_safe_functions.statistics.count_precompute import CountPrecompute
from sail_safe_functions_orchestrator.series_federated import SeriesFederated
from sail_safe_functions_orchestrator.statistics.estimator import Estimator


def count(sample_0: SeriesFederated):
    estimator = Count()
    return estimator.run(sample_0)


class Count(Estimator):
    """
    Class have run method to perform the federated variance.
    """

    def __init__(self) -> None:
        super().__init__(["count"])

    def run(self, sample_0: SeriesFederated):
        """
        counts the lenght of a federated sereies

        :param sample_0: sample to be counted
        :type sample_0: SeriesFederated
        :return: the numer of elements in a series
        :rtype: float
        """
        count = 0
        for dataset_id in sample_0.list_dataset_id:
            client = sample_0.service_client.get_client(dataset_id)
            reference_series_0 = sample_0.get_reference_series(dataset_id)
            count += client.call(CountPrecompute, reference_series_0)
        return count

    def run_reference(self, sample_0: SeriesFederated):
        return sample_0.to_numpy().size
