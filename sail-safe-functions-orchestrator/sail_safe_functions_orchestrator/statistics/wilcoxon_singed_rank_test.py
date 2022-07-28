import numpy
import scipy
from sail_safe_functions.statistics.wilcoxon_singed_rank_test_aggregate import (
    WilcoxonSingedRankTestAggregate,
)
from sail_safe_functions.statistics.wilcoxon_singed_rank_test_precompute import (
    WilcoxonSingedRankTestPrecompute,
)
from sail_safe_functions_orchestrator import preprocessing
from sail_safe_functions_orchestrator.preprocessing.wilcoxon_singed_rank_test_difference_tranform import (
    WilcoxonSingedRankTestDifferenceTranform,
)
from sail_safe_functions_orchestrator.series_federated import SeriesFederated
from sail_safe_functions_orchestrator.statistics.estimator import Estimator


def wilcoxon_singed_rank_test(
    sample_0: SeriesFederated,
    sample_1: SeriesFederated,
    alternative: str,
    type_ranking: str,
):
    estimator = WilcoxonSingedRankTest(alternative, type_ranking)
    return estimator.run(sample_0, sample_1)


class WilcoxonSingedRankTest(Estimator):
    def __init__(self, alternative, type_ranking: str) -> None:
        super().__init__(["w_statistic", "p_value"])
        if alternative not in ["less", "two-sided", "greater"]:
            raise ValueError('Alternative must be of "less", "two-sided" or "greater"')
        if type_ranking not in {"unsafe", "cdf"}:
            raise ValueError("`type_ranking` must be `unsafe` or `cdf`")
        self.alternative = alternative
        self.type_ranking = type_ranking

    def run(self, sample_0: SeriesFederated, sample_1: SeriesFederated):

        if sample_0.size != sample_1.size:
            raise ValueError("`sample_0` and `sample_1` must have the same length.")

        size_sample = sample_0.size
        (
            sample_difference,
            sample_difference_absolute,
        ) = preprocessing.wilcoxon_singed_rank_test_difference_tranform(
            sample_0, sample_1
        )
        sample_difference_absolute_ranked = preprocessing.rank(
            sample_difference_absolute, self.type_ranking
        )

        # Calculating precompute
        list_precompute = []
        for series_difference, series_difference_absolute_ranked in zip(
            sample_difference.dict_series.values(),
            sample_difference_absolute_ranked.dict_series.values(),
        ):
            list_precompute.append(
                WilcoxonSingedRankTestPrecompute.run(
                    series_difference, series_difference_absolute_ranked
                )
            )

        # rank_minus rank_plus
        rank_minus, rank_plus = WilcoxonSingedRankTestAggregate.run(list_precompute)

        if self.alternative == "two-sided":
            w_statistic = min(rank_minus, rank_plus)
        else:
            w_statistic = rank_plus

        mean = size_sample * (size_sample + 1.0) * 0.25
        standard_deviation = numpy.sqrt(
            size_sample * (size_sample + 1.0) * (2.0 * size_sample + 1.0) / 24
        )
        z_statistic = (w_statistic - mean) / standard_deviation

        if self.alternative == "two-sided":
            p_value = 2.0 * scipy.stats.distributions.norm.sf(abs(z_statistic))
        elif self.alternative == "less":
            p_value = scipy.stats.distributions.norm.cdf(z_statistic)
        elif self.alternative == "greater":
            p_value = scipy.stats.distributions.norm.sf(z_statistic)
        else:
            raise Exception()

        return w_statistic, p_value

    def run_reference(self, sample_0: SeriesFederated, sample_1: SeriesFederated):
        # we only do aproximation of T(aproximation does not work very wel below 10) and only do wilcox mode tie resolution
        return scipy.stats.wilcoxon(
            sample_0.to_numpy(),
            sample_1.to_numpy(),
            zero_method="wilcox",
            alternative=self.alternative,
            mode="approx",
        )
