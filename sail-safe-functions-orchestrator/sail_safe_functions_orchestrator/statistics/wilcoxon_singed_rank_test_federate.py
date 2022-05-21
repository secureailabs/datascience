import numpy
import scipy
from sail_safe_functions.statistics.wilcoxon_singed_rank_test_agregate import WilcoxonSingedRankTestAgregate
from sail_safe_functions.statistics.wilcoxon_singed_rank_test_precompute import WilcoxonSingedRankTestPrecompute
from sail_safe_functions_orchestrator.preprocessing.rank_federate import RankFederate
from sail_safe_functions_orchestrator.preprocessing.wilcoxon_singed_rank_test_difference_tranform import (
    WilcoxonSingedRankTestDifferenceTranform,
)
from sail_safe_functions_orchestrator.series_federated import SeriesFederated


class WilcoxonSingedRankTestFederate:
    @staticmethod
    def wilcoxon_singed_rank_test(
        sample_0: SeriesFederated, sample_1: SeriesFederated, alternative: str, type_ranking: str
    ):
        WilcoxonSingedRankTestFederate.run(sample_0, sample_1, alternative, type_ranking)

    @staticmethod
    def run(sample_0: SeriesFederated, sample_1: SeriesFederated, alternative: str, type_ranking: str):

        size_sample = sample_0.size

        if alternative not in ["two-sided", "less", "greater"]:
            raise ValueError("`alternative` must be either `two-sided`, `greater` or `less`")
        if type_ranking not in ["unsafe", "cdf"]:
            raise ValueError("`type_ranking` must be either `unsafe` or `cdf`")
        if sample_0.size != sample_1.size:
            raise ValueError("`sample_0` and `sample_1` must have the same length.")

        sample_difference, sample_difference_absolute = WilcoxonSingedRankTestDifferenceTranform.run(sample_0, sample_1)
        sample_difference_absolute_ranked = RankFederate.run(sample_difference_absolute, type_ranking)

        # Calculating precompute
        list_precompute = []
        for series_difference, series_difference_absolute_ranked in zip(
            sample_difference.dict_series.values(), sample_difference_absolute_ranked.dict_series.values()
        ):
            list_precompute.append(
                WilcoxonSingedRankTestPrecompute.run(series_difference, series_difference_absolute_ranked)
            )

        # rank_minus rank_plus
        rank_minus, rank_plus = WilcoxonSingedRankTestAgregate.run(list_precompute)

        if alternative == "two-sided":
            w_statistic = min(rank_minus, rank_plus)
        else:
            w_statistic = rank_plus

        mean = size_sample * (size_sample + 1.0) * 0.25
        standard_deviation = numpy.sqrt(size_sample * (size_sample + 1.0) * (2.0 * size_sample + 1.0) / 24)
        z_statistic = (w_statistic - mean) / standard_deviation

        if alternative == "two-sided":
            p_value = 2.0 * scipy.stats.distributions.norm.sf(abs(z_statistic))
        elif alternative == "less":
            p_value = scipy.stats.distributions.norm.cdf(z_statistic)
        elif alternative == "greater":
            p_value = scipy.stats.distributions.norm.sf(z_statistic)
        else:
            raise Exception()

        return w_statistic, p_value

    @staticmethod
    def run_reference(sample_0: SeriesFederated, sample_1: SeriesFederated, alternative: str):
        # we only do aproximation of T(aproximation does not work very wel below 10) and only do wilcox mode tie resolution
        return scipy.stats.wilcoxon(
            sample_0.to_numpy(), sample_1.to_numpy(), zero_method="wilcox", alternative=alternative, mode="approx"
        )
