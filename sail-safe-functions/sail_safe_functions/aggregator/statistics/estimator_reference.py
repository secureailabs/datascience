import numpy
from sail_safe_functions.aggregator.series_federated import SeriesFederated
from sail_safe_functions.aggregator.statistics.count import Count
from sail_safe_functions.aggregator.statistics.estimator_one_sample import EstimatorOneSample
from sail_safe_functions.aggregator.statistics.kurtosis import Kurtosis
from sail_safe_functions.aggregator.statistics.mean import Mean
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


class EstimatorReference(EstimatorOneSample):  # TODO make two sample variant
    def __init__(self, estimator: EstimatorOneSample) -> None:
        super().__init__(estimator.estimator_name, estimator.list_estimate_name)
        self.estimator = estimator

    def run(self, sample_0: SeriesFederated):
        if self.estimator.__class__ == Count:
            return run_reference_count(sample_0)

        if self.estimator.__class__ == Mean:
            return run_reference_mean(sample_0)

        if self.estimator.__class__ == Variance:
            return run_reference_variance(sample_0)

        if self.estimator.__class__ == Skewness:
            return run_reference_skewness(sample_0)

        if self.estimator.__class__ == Kurtosis:
            return run_reference_kurtosis(sample_0)

        return self.estimator.run_reference(sample_0)
