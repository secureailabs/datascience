from typing import List, Tuple

import numpy
from sail_core.implementation_manager import ImplementationManager
from sail_safe_functions.aggregator.data_model.data_model_series import DataModelSeries
from sail_safe_functions.aggregator.series_federated import SeriesFederated
from sail_safe_functions.participant.preprocessing.absolute_value import ValueAbsolute
from sail_safe_functions.participant.preprocessing.weighted_sum import SumWeighted


def wilcoxon_singed_rank_test_difference_tranform(
    sample_0: SeriesFederated,
    sample_1: SeriesFederated,
) -> Tuple[SeriesFederated, SeriesFederated]:
    return WilcoxonSingedRankTestDifferenceTranform.run(sample_0, sample_1)


class WilcoxonSingedRankTestDifferenceTranform:
    "Tranform for Wilcoxon Singed Rank Test"

    @staticmethod
    def run(
        sample_0: SeriesFederated,
        sample_1: SeriesFederated,
    ) -> Tuple[SeriesFederated, SeriesFederated]:

        list_reference_sample_difference = []
        list_reference_sample_difference_absolute = []
        service_participant = ImplementationManager.get_instance().get_participant_service()
        for dataset_id in sample_0.list_dataset_id:  # TODO rework abcs #TODO check matching frames

            series_0 = sample_0.dict_reference_series[dataset_id]
            series_1 = sample_1.dict_reference_series[dataset_id]
            reference_series_difference = service_participant.call(
                dataset_id, SumWeighted, [series_0, series_1], [1, -1]
            )
            reference_series_difference_absolute = service_participant.call(
                dataset_id, ValueAbsolute, reference_series_difference
            )
            list_reference_sample_difference.append(reference_series_difference)
            list_reference_sample_difference_absolute.append(reference_series_difference_absolute)

        series_name_sample_difference = "sample_difference"
        data_model_sample_difference = DataModelSeries.create_numerical(
            series_name_sample_difference, -1, None, DataModelSeries.AgregatorComputed
        )

        series_name_sample_difference_absolute = "sample_difference_absolute"
        data_model_sample_difference_absolute = DataModelSeries.create_numerical(
            series_name_sample_difference_absolute, -1, None, DataModelSeries.AgregatorComputed
        )

        sample_difference = SeriesFederated(list_reference_sample_difference, data_model_sample_difference)
        sample_difference_absolute = SeriesFederated(
            list_reference_sample_difference_absolute, data_model_sample_difference_absolute
        )

        return sample_difference, sample_difference_absolute
