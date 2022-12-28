from sail_core.implementation_manager import ImplementationManager
from sail_safe_functions.aggregator.data_model.data_model_series import DataModelSeries
from sail_safe_functions.aggregator.series_federated import SeriesFederated
from sail_safe_functions.aggregator.tools_common import check_instance
from sail_safe_functions.participant.preprocessing.concatenate_precompute import ConcatenatePrecompute


def concatenate(sample_0: SeriesFederated, sample_1: SeriesFederated) -> SeriesFederated:
    return Concatenate.run(sample_0, sample_1)


class Concatenate:
    """Federate wrapper safe function for the pandas concatenate"""

    @staticmethod
    def run(sample_0: SeriesFederated, sample_1: SeriesFederated):
        check_instance(sample_0, SeriesFederated)
        check_instance(sample_1, SeriesFederated)
        list_reference = []
        series_name = sample_0.series_name + "_" + sample_1.series_name + "_concatinated"
        data_model_series = DataModelSeries.create_numerical(series_name, -1, None, DataModelSeries.AgregatorComputed)

        participant_service = ImplementationManager.get_instance().get_participant_service()
        for dataset_id in sample_0.list_dataset_id:  # TODO rework abcs

            series_0 = sample_0.dict_reference_series[dataset_id]
            series_1 = sample_1.dict_reference_series[dataset_id]
            list_reference.append(
                participant_service.call(dataset_id, ConcatenatePrecompute, series_0, series_1, data_model_series)
            )
        return SeriesFederated(list_reference, data_model_series)
