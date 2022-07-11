from sail_safe_functions_orchestrator.series_federated import SeriesFederated


class Estimator:
    def __init__(self) -> None:
        pass

    def run(self, sample_0: SeriesFederated):
        raise NotImplementedError()

    def run_reference(self, sample_0: SeriesFederated):
        raise NotImplementedError()
