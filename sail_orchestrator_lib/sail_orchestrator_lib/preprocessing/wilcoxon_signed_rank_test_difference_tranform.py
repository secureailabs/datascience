from typing import List, Tuple

import numpy
from sail_safe_functions.preprocessing.absolute_value import ValueAbsolute
from sail_safe_functions.preprocessing.weighted_sum import SumWeighted
from sail_safe_functions_orchestrator.series_federated import SeriesFederated
from sail_safe_functions_test.helper_sail_safe_functions.series_federated_local import (
    SeriesFederatedLocal,
)


def wilcoxon_singed_rank_test_difference_tranform(
    sample_0: SeriesFederated, sample_1: SeriesFederated
) -> Tuple[List[float], List[float]]:
    return WilcoxonSingedRankTestDifferenceTranform.run(sample_0, sample_1)


class WilcoxonSingedRankTestDifferenceTranform:
    "Tranform for Wilcoxon Singed Rank Test"

    @staticmethod
    def run(
        sample_0: SeriesFederated, sample_1: SeriesFederated
    ) -> Tuple[List[float], List[float]]:

        sample_difference = SeriesFederatedLocal()  # TODO make transforms smarter
        sample_difference_absolute = (
            SeriesFederatedLocal()
        )  # TODO make transforms smarter
        for (
            dataset_id
        ) in sample_0.dict_series:  # TODO rework abcs #TODO check matching frames
            series_0 = sample_0.dict_series[dataset_id]
            series_1 = sample_1.dict_series[dataset_id]
            series_difference = SumWeighted.run([series_0, series_1], [1, -1])
            series_difference_absolute = ValueAbsolute.run(series_difference)
            sample_difference.add_series(dataset_id, series_difference)
            sample_difference_absolute.add_series(
                sample_difference_absolute, series_difference_absolute
            )

        return sample_difference, sample_difference_absolute
