from sail_safe_functions.preprocessing.concatenate_precompute import ConcatenatePrecompute
from sail_safe_functions_orchestrator.series_federated import SeriesFederated
from sail_safe_functions_orchestrator.tools_common import ToolsCommon


def concatenate(sample_0: SeriesFederated, sample_1: SeriesFederated) -> SeriesFederated:
    return Concatenate.run(sample_0, sample_1)


class Concatenate:
    """Federate wrapper safe function for the pandas concatenate"""

    def run(sample_0: SeriesFederated, sample_1: SeriesFederated):
        ToolsCommon.check_instance(sample_0, SeriesFederated)
        ToolsCommon.check_instance(sample_1, SeriesFederated)
        sample_concatenated = sample_0.create_new()

        for dataset_id in sample_0.dict_series:  # TODO rework abcs
            series_0 = sample_0.dict_series[dataset_id]
            series_1 = sample_1.dict_series[dataset_id]
            sample_concatenated.add_series(dataset_id, ConcatenatePrecompute.run(series_0, series_1))
        return sample_concatenated