from sail_safe_functions_orchestrator.series_federated import SeriesFederated
from sail_safe_functions_orchestrator.statistics.estimator import Estimator


class EstimatorReference(Estimator):
    def __init__(self, estimator: Estimator) -> None:
        super().__init__()
        self.estimator = estimator

    def run(self, sample_0: SeriesFederated):
        return self.estimator.run_reference(sample_0)
