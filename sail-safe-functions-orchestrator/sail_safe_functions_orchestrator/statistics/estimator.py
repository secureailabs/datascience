from sail_safe_functions_orchestrator.series_federated import SeriesFederated


class Estimator:
    def __init__(self, list_name_estimate) -> None:
        self.list_name_estimate = list_name_estimate

    def Run(self, sample_0: SeriesFederated):
        raise NotImplementedError()

    def run_reference(self, sample_0: SeriesFederated):
        raise NotImplementedError()
