from typing import Tuple

import numpy
from sail_safe_functions.statistics.covariance_aggregate import \
    CovarianceAggregate
from sail_safe_functions.statistics.covariance_precompute import \
    CovariancePrecompute
from sail_safe_functions_orchestrator.series_federated import SeriesFederated
from sail_safe_functions_orchestrator.statistics.estimator import Estimator


def covariance(sample_0: SeriesFederated, sample_1: SeriesFederated) -> float:
    """
    covariance is defined as ((x_i - x_mean) * (y_i - y_mean)) / n -1

    :param sample_0: sample_0
    :type sample_0: SeriesFederated
    :param sample_1: sample_1
    :type sample_1: SeriesFederated
    :return: covarriance value

    """
    estimator = Covariance()
    return estimator.run(sample_0, sample_1)


class Covariance(Estimator):
    """
    Estimator for covariance
    """

    def __init__(self) -> None:
        super().__init__(["covariance"])

    def run(self, sample_0: SeriesFederated, sample_1: SeriesFederated) -> Tuple[float, float]:

        list_precompute = []
        list_key_dataframe = list(sample_0.dict_series.keys())
        for key_dataframe in list_key_dataframe:
            list_precompute.append(
                CovariancePrecompute.run(
                    sample_0.dict_series[key_dataframe],
                    sample_1.dict_series[key_dataframe],
                )
            )
        return CovarianceAggregate.run(list_precompute)

    def run_reference(self, sample_0: SeriesFederated, sample_1: SeriesFederated) -> Tuple[float, float]:
        return numpy.cov(sample_0.to_numpy(), sample_1.to_numpy())[0, 1]
