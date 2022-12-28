from typing import Tuple

import numpy
import scipy
from sail_core.implementation_manager import ImplementationManager
from sail_safe_functions.aggregator import preprocessing, statistics
from sail_safe_functions.aggregator.series_federated import SeriesFederated
from sail_safe_functions.aggregator.statistics.estimator import Estimator
from sail_safe_functions.aggregator.tools_common import check_instance
from sail_safe_functions.participant.statistics.mann_whitney_u_test_precompute import MannWhitneyUTestPrecompute
from scipy import stats


def mann_whitney_u_test(
    sample_0: SeriesFederated,
    sample_1: SeriesFederated,
    alternative: str,
    type_ranking: str,
):
    estimator = MannWhitneyUTest(alternative, type_ranking)
    return estimator.run(sample_0, sample_1)


class MannWhitneyUTest(Estimator):
    """
    Federated version of the mann whiney u test, it makes two compromised
    1. Tie correction was removed, it has a small impact most of the time. The reference implementation still does this.
    2. The p values is always computed asymptotoicly, exact methods is only feasable for small smalle sizes.
    """

    def __init__(
        self,
        alternative: str,
        type_ranking: str,
    ) -> None:
        super().__init__(["f_statistic", "p_value"])
        if alternative not in ["less", "two-sided", "greater"]:
            raise ValueError('Alternative must be of "less", "two-sided" or "greater"')
        if type_ranking not in {"unsafe", "cdf"}:
            raise ValueError("`type_ranking` must be `unsafe` or `cdf`")
        self.alternative = alternative
        self.type_ranking = type_ranking

    def run(self, sample_0: SeriesFederated, sample_1: SeriesFederated) -> Tuple[float, float]:
        """
        It takes two federated series, and returns the p-value and test statistic of the mann whitney u test

        :param sample_0: First sample series
        :type sample_0: SeriesFederated
        :param sample_1: Two sample series
        :type sample_1: SeriesFederated
        :return: _description_
        :rtype: Tuple[float, float]
        """
        check_instance(sample_0, SeriesFederated)
        check_instance(sample_1, SeriesFederated)
        n0 = statistics.count(sample_0)
        n1 = statistics.count(sample_1)

        sample_concatenated = preprocessing.concatenate(sample_0, sample_1)
        sample_concatenated_ranked = preprocessing.rank(sample_concatenated, self.type_ranking)

        list_precompute = []
        participant_service = ImplementationManager.get_instance().get_participant_service()
        for dataset_id in sample_0.list_dataset_id:
            series_0 = sample_0.dict_reference_series[dataset_id]
            series_concatenated_ranked = sample_concatenated_ranked.dict_reference_series[dataset_id]
            list_precompute.append(
                participant_service.call(dataset_id, MannWhitneyUTestPrecompute, series_0, series_concatenated_ranked)
            )

        sum_ranks_0 = numpy.array(list_precompute).sum()

        U0 = sum_ranks_0 - n0 * (n0 + 1) / 2
        U1 = n0 * n1 - U0

        mean = ((n0 * n1) + 1) / 2
        standard_deviation = numpy.sqrt(n0 * n1 / 12 * ((n0 + n1 + 1)))
        if self.alternative == "two-sided":
            U = numpy.maximum(U0, U1)
        elif self.alternative == "greater":
            U = U0
        elif self.alternative == "less":
            U = U1
        else:
            raise Exception

        z = (U - mean) / standard_deviation
        p = scipy.stats.norm.sf(z)
        if self.alternative == "two-sided":
            p *= 2

        # Ensure that test statistic is not greater than 1
        # This could happen for exact test when U = m*n/2
        p = numpy.clip(p, 0, 1)

        return U0, p

    def run_reference(
        self,
        sample_0: SeriesFederated,
        sample_1: SeriesFederated,
    ):
        return stats.mannwhitneyu(
            sample_0.to_numpy(),
            sample_1.to_numpy(),
            alternative=self.alternative,
            method="asymptotic",
        )
