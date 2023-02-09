from typing import Tuple

import numpy
from sail_safe_functions.aggregator.series_federated import SeriesFederated
from sail_safe_functions.aggregator.statistics.count import Count
from sail_safe_functions.aggregator.statistics.estimator_one_sample import EstimatorOneSample
from sail_safe_functions.aggregator.statistics.kolmogorov_smirnov_test import KolmogorovSmirnovTest
from sail_safe_functions.aggregator.statistics.kurtosis import Kurtosis
from sail_safe_functions.aggregator.statistics.mean import Mean
from sail_safe_functions.aggregator.statistics.min_max import MinMax
from sail_safe_functions.aggregator.statistics.skewness import Skewness
from sail_safe_functions.aggregator.statistics.variance import Variance
from scipy import stats


def run_reference_count(
    sample_0: SeriesFederated,
) -> float:
    return sample_0.to_numpy().size


def run_reference_mean(
    sample_0: SeriesFederated,
) -> float:
    return numpy.mean(sample_0.to_numpy())


def run_reference_variance(
    sample_0: SeriesFederated,
) -> float:
    return numpy.var(sample_0.to_numpy(), ddof=1)


def run_reference_skewness(
    sample_0: SeriesFederated,
) -> float:
    return float(stats.skew(sample_0.to_numpy()))


def run_reference_kurtosis(
    sample_0: SeriesFederated,
) -> float:
    return float(stats.kurtosis(sample_0.to_numpy()))


def run_reference_kolmogorov_smirnov_test(
    sample_0: SeriesFederated,
    type_distribution: str,
) -> Tuple[float, float]:
    if type_distribution == "normalunit":
        return stats.kstest(sample_0.to_numpy(), "norm")
    else:
        raise NotImplementedError()


def run_reference_min_max(
    sample_0: SeriesFederated,
) -> Tuple[float, float]:
    min_numpy = numpy.min(sample_0.to_numpy())
    max_numpy = numpy.max(sample_0.to_numpy())
    return min_numpy, max_numpy


class EstimatorOneSampleReference(EstimatorOneSample):
    def __init__(
        self,
        estimator: EstimatorOneSample,
    ) -> None:
        super().__init__(f"{estimator.estimator_name} - reference", estimator.list_estimate_name)
        self.__estimator = estimator

    def run(
        self,
        sample_0: SeriesFederated,
    ):
        if self.__estimator.__class__ == Count:
            return run_reference_count(sample_0)

        if self.__estimator.__class__ == Mean:
            return run_reference_mean(sample_0)

        if self.__estimator.__class__ == Variance:
            return run_reference_variance(sample_0)

        if self.__estimator.__class__ == Skewness:
            return run_reference_skewness(sample_0)

        if self.__estimator.__class__ == Kurtosis:
            return run_reference_kurtosis(sample_0)

        if self.__estimator.__class__ == KolmogorovSmirnovTest:
            return run_reference_kolmogorov_smirnov_test(
                sample_0, self.__estimator.type_distribution
            )  # TODO hide parameters

        if self.__estimator.__class__ == MinMax:
            return run_reference_min_max(sample_0)

        raise Exception(f"no reference estimator for class {str(self.__estimator.__class__.__name__)}")
