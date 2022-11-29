import numpy
from sail_safe_functions.statistics.variance_aggregate import VarianceAggregate
from sail_safe_functions.statistics.variance_precompute import VariancePrecompute
from sail_safe_functions_orchestrator.series_federated import SeriesFederated
from sail_safe_functions_orchestrator.statistics.estimator import Estimator


def variance(sample_0: SeriesFederated):
    estimator = Variance()
    return estimator.run(sample_0)


class Variance(Estimator):
    """
    Class have run method to perform the federated variance.
    """

    def __init__(self) -> None:
        super().__init__(["variance"])

    def run(self, sample_0: SeriesFederated):
        """
        It takes one federated series, and returns the variance of the series

        :param sample_0: _description_
        :type sample_0: SeriesFederated
        :return: _description_
        :rtype: _type_
        """
        list_list_precompute = []
        for dataset_id in sample_0.list_dataset_id:
            client = sample_0.service_client.get_client(dataset_id)
            reference_series_0 = sample_0.get_reference_series(dataset_id)
            list_list_precompute.append(client.call(VariancePrecompute, reference_series_0))
        variance = VarianceAggregate.run(list_list_precompute)
        return variance

    def run_reference(self, sample_0: SeriesFederated):
        return numpy.var(sample_0.to_numpy(), ddof=1)
