from sail_safe_functions.preprocessing.concatenate import Concatenate
from sail_safe_functions_test.helper_sail_safe_functions.series_federated_local import SeriesFederatedLocal


class ConcatenateFederate:
    """Federate wrapper safe function for the pandas concatenate"""

    def run(sample_0: SeriesFederatedLocal, sample_1: SeriesFederatedLocal):
        sample_concatenated = SeriesFederatedLocal()  # TODO make transforms smarter

        for dataset_id in sample_0.dict_series:  # TODO rework abcs
            series_0 = sample_0.dict_series[dataset_id]
            series_1 = sample_1.dict_series[dataset_id]
            sample_concatenated.add_series(dataset_id, Concatenate.run(series_0, series_1))
        return sample_concatenated
