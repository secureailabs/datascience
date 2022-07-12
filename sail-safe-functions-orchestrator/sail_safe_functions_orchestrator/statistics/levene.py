from typing import Tuple

from sail_safe_functions.statistics.levene_agregate import LeveneAgregate
from sail_safe_functions.statistics.levene_precompute import LevenePrecompute
from sail_safe_functions_orchestrator.series_federated import SeriesFederated
from sail_safe_functions_orchestrator.statistics.estimator import Estimator
from sail_safe_functions_orchestrator.statistics.mean import Mean
from scipy import stats
from scipy.stats import distributions


class Levene(Estimator):
    """
    This class contains the fedrated Levenes method

    :return: f_statistic(statistics from levenes test)  , p-value
    :rtype: float
    """

    @staticmethod
    def levene(
        sample_0: SeriesFederated,
        sample_1: SeriesFederated,
    ) -> Tuple[float, float]:
        """
        This the main function where Levenes Fedration happens

        :param sample_0: fedrated series
        :type sample_0: SeriesFederated
        :param sample_1: _description_
        :type sample_1:  fedrsated series
        :return: F-stat, p-value
        :rtype: Tuple[float, float]
        """
        estimator = Levene()
        return estimator.run(sample_0, sample_1)

    def __init__(self) -> None:
        super().__init__(["f_statistic", "p_value"])

    def run(self, sample_0: SeriesFederated, sample_1: SeriesFederated):
        mean_sample_0 = Mean.mean(sample_0)
        mean_sample_1 = Mean.mean(sample_1)

        list_list_precompute = []
        list_key_dataframe = list(sample_0.dict_series.keys())
        # TODO deal with posibilty sample_0 and sample_1 do net share same child frames
        for key_dataframe in list_key_dataframe:
            list_list_precompute.append(
                LevenePrecompute.run(
                    sample_0.dict_series[key_dataframe],
                    sample_1.dict_series[key_dataframe],
                    mean_sample_0,
                    mean_sample_1,
                )
            )

        f_statistic, dof = LeveneAgregate.run(list_list_precompute)
        p_value = distributions.f.sf(f_statistic, 1, dof)  # 1 - cdf
        return f_statistic, p_value

    def run_reference(self, sample_0: SeriesFederated, sample_1: SeriesFederated):
        return stats.levene(sample_0.to_numpy(), sample_1.to_numpy(), center="mean")
