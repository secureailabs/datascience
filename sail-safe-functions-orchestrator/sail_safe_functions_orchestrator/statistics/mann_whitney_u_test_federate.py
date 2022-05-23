from typing import Tuple

import numpy
import scipy
from sail_safe_functions.statistics.mann_whitney_u_test_agregate import MannWhitneyUTestAgregate
from sail_safe_functions.statistics.mann_whitney_u_test_precompute import MannWhitneyUTestPrecompute
from sail_safe_functions_orchestrator.preprocessing.concatenate_federate import ConcatenateFederate
from sail_safe_functions_orchestrator.preprocessing.rank_federate import RankFederate
from sail_safe_functions_orchestrator.series_federated import SeriesFederated
from scipy.stats import mannwhitneyu


class MannWhitneyUTestFederate:
    """
    Federated version of the mann whiney u test, it makes two compromised
    1. Tie correction was removed, it has a small impact most of the time. The reference implementation still does this.
    2. The p values is always computed asymptotoicly, exact methods is only feasable for small smalle sizes.
    """

    def mann_whitney_u_test(sample_0: SeriesFederated, sample_1: SeriesFederated, alternative: str, type_ranking: str):
        return MannWhitneyUTestFederate.run(sample_0, sample_1, alternative, type_ranking)

    def run(
        sample_0: SeriesFederated, sample_1: SeriesFederated, alternative: str, type_ranking: str
    ) -> Tuple[float, float]:
        n0, n1 = sample_0.size, sample_1.size

        sample_concatenated = ConcatenateFederate.run(sample_0, sample_1)
        sample_concatenated_ranked = RankFederate.run(sample_concatenated, type_ranking)

        list_precompute = []
        for dataset_id in sample_0.dict_series:
            series_0 = sample_0.dict_series[dataset_id]
            series_concatenated_ranked = sample_concatenated_ranked.dict_series[dataset_id]
            list_precompute.append(MannWhitneyUTestPrecompute.run(series_0, series_concatenated_ranked))

        sum_ranks_0 = MannWhitneyUTestAgregate.run(list_precompute)

        U0 = sum_ranks_0 - n0 * (n0 + 1) / 2
        U1 = n0 * n1 - U0

        mean = ((n0 * n1) + 1) / 2
        standard_deviation = numpy.sqrt(n0 * n1 / 12 * ((n0 + n1 + 1)))
        if alternative == "two-sided":
            U = numpy.maximum(U0, U1)
        elif alternative == "greater":
            U = U0
        elif alternative == "less":
            U = U1
        else:
            raise Exception

        z = (U - mean) / standard_deviation
        p = scipy.stats.norm.sf(z)
        if alternative == "two-sided":
            p *= 2

        # Ensure that test statistic is not greater than 1
        # This could happen for exact test when U = m*n/2
        p = numpy.clip(p, 0, 1)

        return U0, p

    def run_reference(
        sample_0: SeriesFederated,
        sample_1: SeriesFederated,
        alternative: str,
    ):
        return mannwhitneyu(sample_0.to_numpy(), sample_1.to_numpy(), alternative=alternative, method="asymptotic")
