from typing import Tuple

import numpy
from sail_safe_functions.aggregator.series_federated import SeriesFederated
from sail_safe_functions.aggregator.statistics.chisquare import Chisquare
from sail_safe_functions.aggregator.statistics.estimator_two_sample import EstimatorTwoSample
from sail_safe_functions.aggregator.statistics.levene_test import LeveneTest
from sail_safe_functions.aggregator.statistics.mann_whitney_u_test import MannWhitneyUTest
from sail_safe_functions.aggregator.statistics.paired_t_test import PairedTTest
from sail_safe_functions.aggregator.statistics.pearson import Pearson
from sail_safe_functions.aggregator.statistics.spearman import Spearman
from sail_safe_functions.aggregator.statistics.student_t_test import StudentTTest
from sail_safe_functions.aggregator.statistics.welch_t_test import WelchTTest
from sail_safe_functions.aggregator.statistics.wilcoxon_signed_rank_test import WilcoxonSingedRankTest
from scipy import stats


def run_reference_pearson(
    sample_0: SeriesFederated,
    sample_1: SeriesFederated,
) -> Tuple[float, float]:
    return stats.pearsonr(sample_0.to_numpy(), sample_1.to_numpy())


def run_reference_chisquare(
    sample_0: SeriesFederated,
    sample_1: SeriesFederated,
) -> Tuple[float, float]:
    count_total = sample_0.to_numpy().size

    array_0 = list(sample_0.to_numpy())
    array_1 = list(sample_1.to_numpy())
    list_unique_0 = numpy.unique(array_0).tolist()
    list_unique_1 = numpy.unique(array_1).tolist()
    array_true = numpy.zeros((len(list_unique_0), len(list_unique_1)))
    array_pred = numpy.zeros((len(list_unique_0), len(list_unique_1)))

    for i in range(len(array_0)):
        index_0 = list_unique_0.index(array_0[i])
        index_1 = list_unique_1.index(array_1[i])
        array_true[index_0, index_1] += 1

    for i_0 in range(len(list_unique_0)):
        for i_1 in range(len(list_unique_1)):
            array_pred[i_0, i_1] = array_true[i_0, :].sum() * array_true[:, i_1].sum() / count_total

    ddof = -((len(list_unique_0) - 1) * (len(list_unique_1) - 1)) + (len(array_true.ravel()) - 1)  # 2d instead of 1d
    chisquare_statistic, p_value = stats.chisquare(array_true.ravel(), f_exp=array_pred.ravel(), ddof=ddof)
    return chisquare_statistic, p_value


def run_reference_spearman(
    sample_0: SeriesFederated,
    sample_1: SeriesFederated,
    alternative: str,
) -> Tuple[float, float]:
    return stats.spearmanr(sample_0.to_numpy(), sample_1.to_numpy(), alternative=alternative)


def run_reference_levene_test(
    sample_0: SeriesFederated,
    sample_1: SeriesFederated,
) -> Tuple[float, float]:
    return stats.levene(sample_0.to_numpy(), sample_1.to_numpy(), center="mean")


def run_reference_mann_whitney_u_test(
    sample_0: SeriesFederated,
    sample_1: SeriesFederated,
    alternative: str,
) -> Tuple[float, float]:
    return stats.mannwhitneyu(
        sample_0.to_numpy(),
        sample_1.to_numpy(),
        alternative=alternative,
        method="asymptotic",
    )


def run_reference_student_t_test(
    sample_0: SeriesFederated,
    sample_1: SeriesFederated,
    alternative: str,
) -> Tuple[float, float]:
    return stats.ttest_ind(
        sample_0.to_numpy(),
        sample_1.to_numpy(),
        equal_var=True,
        alternative=alternative,
    )


def run_reference_paired_t_test(
    sample_0: SeriesFederated,
    sample_1: SeriesFederated,
    alternative: str,
) -> Tuple[float, float]:
    return stats.ttest_rel(sample_0.to_numpy(), sample_1.to_numpy(), alternative=alternative)


def run_reference_welch_t_test(
    sample_0: SeriesFederated,
    sample_1: SeriesFederated,
    alternative: str,
) -> Tuple[float, float]:
    return stats.ttest_ind(
        sample_0.to_numpy(),
        sample_1.to_numpy(),
        equal_var=False,
        alternative=alternative,
    )


def run_reference_wilcoxon_singed_rank_test(
    sample_0: SeriesFederated,
    sample_1: SeriesFederated,
    alternative: str,
) -> Tuple[float, float]:
    # we only do aproximation of T(aproximation does not work very well below 10) and only do wilcox mode tie resolution (zero_method)
    return stats.wilcoxon(
        sample_0.to_numpy(),
        sample_1.to_numpy(),
        zero_method="wilcox",
        alternative=alternative,
        mode="approx",
    )


class EstimatorTwoSampleReference(EstimatorTwoSample):
    def __init__(
        self,
        estimator: EstimatorTwoSample,
    ) -> None:
        super().__init__(estimator.estimator_name, estimator.list_estimate_name)
        self.__estimator = estimator

    def run(
        self,
        sample_0: SeriesFederated,
        sample_1: SeriesFederated,
    ):
        if self.__estimator.__class__ == Pearson:
            return run_reference_pearson(sample_0, sample_1)

        if self.__estimator.__class__ == Spearman:
            return run_reference_spearman(sample_0, sample_1, self.__estimator.alternative)  # TODO hide parameters

        if self.__estimator.__class__ == Chisquare:
            return run_reference_chisquare(sample_0, sample_1)

        if self.__estimator.__class__ == LeveneTest:
            return run_reference_levene_test(sample_0, sample_1)

        if self.__estimator.__class__ == MannWhitneyUTest:
            return run_reference_mann_whitney_u_test(sample_0, sample_1, self.__estimator.alternative)

        if self.__estimator.__class__ == WilcoxonSingedRankTest:
            return run_reference_wilcoxon_singed_rank_test(sample_0, sample_1, self.__estimator.alternative)

        if self.__estimator.__class__ == StudentTTest:
            return run_reference_student_t_test(sample_0, sample_1, self.__estimator.alternative)

        if self.__estimator.__class__ == PairedTTest:
            return run_reference_paired_t_test(sample_0, sample_1, self.__estimator.alternative)

        if self.__estimator.__class__ == WelchTTest:
            return run_reference_welch_t_test(sample_0, sample_1, self.__estimator.alternative)

        raise Exception(f"no reference estimator for class {str(self.__estimator.__class__.__name__)}")
