from typing import Tuple

import numpy
from sail_core.implementation_manager import ImplementationManager
from sail_safe_functions.aggregator import preprocessing, statistics
from sail_safe_functions.aggregator.series_federated import SeriesFederated
from sail_safe_functions.aggregator.statistics.estimator_one_sample import EstimatorOneSample
from sail_safe_functions.participant.statistics.kolmogorov_smirnov_test_precompute import (
    KolmogorovSmirnovTestPrecompute,
)
from scipy import stats
from scipy.stats import kstwo


def kolmogorov_smirnov_test(
    sample_0: SeriesFederated,
    type_distribution: str,
    type_ranking: str,
) -> Tuple[float, float]:
    """
    Perform federated kolmogorov_smirnov test.
    Executes a kolmogorov_smirnov test checking if sample 0 follows the given distribution.

    :param sample_0: sample to be tested
    :type sample_0: SeriesFederated
    :param type_distribution: type of ranking employed
    :type type_distribution: str
    :param type_ranking: type of rankign employed
    :type type_ranking: str

    :raises ValueError: raise a ValueError if `type_distribution` is not `normal` or `normalunit`
    :raises ValueError: raise a ValueError if `type_ranking` is not  `unsafe` or `cdf`
    :return: returns the k-statistic and the p-value
    :rtype: Tuple[float, float]
    """
    estimator = KolmogorovSmirnovTest(type_distribution, type_ranking)
    return estimator.run(sample_0)


class KolmogorovSmirnovTest(EstimatorOneSample):

    """
    Federated version of the KolmogorovSmirnovFederate test
    """

    def __init__(
        self,
        type_distribution: str,
        type_ranking: str,
    ) -> None:
        super().__init__(f"KolmogorovSmirnovTest - {type_distribution} - {type_ranking}", ["k_statistic", "p_value"])

        if type_distribution not in {"normal", "normalunit"}:
            raise ValueError("`type_distribution` must be `normal` or `normalunit`")
        if type_ranking not in {"unsafe", "cdf"}:
            raise ValueError("`type_ranking` must be `unsafe` or `cdf`")
        self.type_distribution = type_distribution
        self.type_ranking = type_ranking

    def run(
        self,
        sample_0: SeriesFederated,
    ) -> Tuple[float, float]:
        if self.type_distribution == "normal":
            sample_mean = statistics.mean(sample_0)
            sample_standart_deviation = numpy.sqrt(statistics.variance(sample_0))
            distribution = {
                "type_distribution": self.type_distribution,
                "sample_mean": sample_mean,
                "sample_standart_deviation": sample_standart_deviation,
            }
        elif self.type_distribution == "normalunit":
            distribution = {"type_distribution": self.type_distribution}
        else:
            raise Exception()
        size_sample = statistics.count(sample_0)

        sample_0_ranked = preprocessing.rank(sample_0, type_ranking=self.type_ranking)
        list_precompute = []
        participant_service = ImplementationManager.get_instance().get_participant_service()
        for dataset_id in sample_0.list_dataset_id:
            reference_series_0 = sample_0.dict_reference_series[dataset_id]
            reference_series_0_ranked = sample_0_ranked.dict_reference_series[dataset_id]
            list_precompute.append(
                participant_service.call(
                    dataset_id,
                    KolmogorovSmirnovTestPrecompute,
                    reference_series_0,
                    reference_series_0_ranked,
                    distribution,
                    size_sample,
                )
            )

        k_statistic = max(list_precompute)

        p_value = float(kstwo.sf(k_statistic, size_sample))

        return k_statistic, p_value
