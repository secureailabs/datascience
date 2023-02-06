import numpy
from sail_safe_functions.aggregator.series_federated import SeriesFederated
from sail_safe_functions.aggregator.statistics.estimator_one_sample import EstimatorOneSample
from sail_safe_functions.participant.statistics.count_precompute import CountPrecompute


def count(sample_0: SeriesFederated):
    estimator = Count()
    return estimator.run(sample_0)


class Count(EstimatorOneSample):
    """
    Class have run method to perform the federated variance.
    """

    def __init__(self) -> None:
        super().__init__("Count", ["count"])

    def run(self, sample_0: SeriesFederated):
        """
        counts the lenght of a federated sereies

        :param sample_0: sample to be counted
        :type sample_0: SeriesFederated
        :return: the numer of elements in a series
        :rtype: float
        """
        list_precompute = sample_0.map_function(CountPrecompute)
        return sum(list_precompute)
