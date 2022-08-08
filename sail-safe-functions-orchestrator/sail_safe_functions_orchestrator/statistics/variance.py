import numpy
import pandas
from sail_safe_functions.statistics.variance_aggregate import VarianceAggregate
from sail_safe_functions.statistics.variance_precompute import VariancePrecompute
from sail_safe_functions_orchestrator.series_federated import SeriesFederated
from sail_safe_functions_orchestrator.statistics.estimator import Estimator


def variance(sample_0: SeriesFederated):
    estimator = Variance()
    return estimator.run(sample_0)


class Variance(Estimator):
    def __init__(self) -> None:
        super().__init__(["variance"])

    def run(self, sample_0: SeriesFederated):
        """
        Runs federated Mean function

        :param sample_0: _description_
        :type sample_0: SeriesFederated
        :return: _description_
        :rtype: _type_
        """
        list_list_precompute = []
        for series in sample_0.dict_series.values():
            list_list_precompute.append(VariancePrecompute.run(series))
        variance = VarianceAggregate.run(list_list_precompute)
        return variance

    def run_reference(self, sample_0: SeriesFederated):
        return numpy.var(sample_0.to_numpy(), ddof=1)
