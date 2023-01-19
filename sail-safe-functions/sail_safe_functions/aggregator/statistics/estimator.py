from abc import ABC, abstractmethod

from sail_safe_functions.aggregator.series_federated import SeriesFederated


class Estimator(ABC):
    def __init__(self, list_name_estimate) -> None:
        self.list_name_estimate = list_name_estimate

    @abstractmethod
    def run(self, sample_0: SeriesFederated):
        raise NotImplementedError()

    @abstractmethod
    def run_reference(self, sample_0: SeriesFederated):
        raise NotImplementedError()
