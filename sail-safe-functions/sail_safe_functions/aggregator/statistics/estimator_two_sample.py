from abc import abstractmethod
from typing import List

from sail_safe_functions.aggregator.series_federated import SeriesFederated
from sail_safe_functions.aggregator.statistics.estimator import Estimator


class EstimatorTwoSample(Estimator):
    def __init__(self, estimator_name: str, list_estimate_name: List[str]) -> None:
        super().__init__(estimator_name, list_estimate_name)

    @abstractmethod
    def run(self, sample_0: SeriesFederated, sample_1: SeriesFederated):
        raise NotImplementedError()
