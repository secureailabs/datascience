from typing import Tuple

import numpy
from sail_safe_functions.statistics.kolmogorov_smirnov_test_agregate import KolmogorovSmirnovTestAgregate
from sail_safe_functions.statistics.kolmogorov_smirnov_test_precompute import KolmogorovSmirnovTestPrecompute
from sail_safe_functions_orchestrator.preprocessing.rank_federate import RankFederate
from sail_safe_functions_orchestrator.series_federated import SeriesFederated
from sail_safe_functions_orchestrator.statistics.mean_federate import MeanFederate
from sail_safe_functions_orchestrator.statistics.variance_federate import VarianceFederate
from scipy import stats
from scipy.stats import kstwo


class KolmogorovSmirnovTestFederate:

    """
    Federated version of the KolmogorovSmirnovFederate test
    """

    @staticmethod
    def kolmogorov_smirnov(sample_0: SeriesFederated, type_distribution: str, type_ranking: str) -> Tuple[float, float]:
        """Executes a kolmogorov_smirnov test checking if sample 0 follows the given distribution


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
        if type_distribution not in {"normal", "normalunit"}:
            raise ValueError("`type_distribution` must be `normal` or `normalunit`")
        if type_ranking not in {"unsafe", "cdf"}:
            raise ValueError("`type_ranking` must be `unsafe` or `cdf`")
        size_sample = sample_0.size

        if type_distribution == "normal":
            sample_mean = MeanFederate(sample_0)
            sample_standart_deviation = numpy.sqrt(VarianceFederate(sample_0))
            distribution = {
                "type_distribution": type_distribution,
                "sample_mean": sample_mean,
                "sample_standart_deviation": sample_standart_deviation,
            }
        elif type_distribution == "normalunit":
            distribution = {"type_distribution": type_distribution}
        else:
            raise Exception()

        series_sample_ranked_0 = RankFederate.run(sample_0, mode=type_ranking)
        list_list_precompute = []
        for series, series_ranked in zip(sample_0.dict_series.values(), series_sample_ranked_0.dict_series.values()):
            list_list_precompute.append(
                KolmogorovSmirnovTestPrecompute.run(series, series_ranked, distribution, size_sample)
            )
        k_statistic = KolmogorovSmirnovTestAgregate.run(list_list_precompute)

        p_value = kstwo.sf(k_statistic, size_sample)

        return k_statistic, p_value

    @staticmethod
    def run(sample_0: SeriesFederated, type_distribution: str, type_ranking: str) -> Tuple[float, float]:
        return KolmogorovSmirnovTestFederate.kolmogorov_smirnov(sample_0, type_distribution, type_ranking)

    @staticmethod
    def run_reference(
        sample_0: SeriesFederated,
        type_distribution: str,
    ) -> Tuple[float, float]:
        if type_distribution == "normalunit":
            return stats.kstest(sample_0.to_numpy(), "norm")
        else:
            raise Exception()
