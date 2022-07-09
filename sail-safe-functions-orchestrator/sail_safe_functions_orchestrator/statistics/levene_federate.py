from typing import Tuple

from sail_safe_functions.statistics.levene_agregate import LeveneAgregate
from sail_safe_functions.statistics.levene_precompute import LevenePrecompute
from sail_safe_functions_orchestrator.series_federated import SeriesFederated
from sail_safe_functions_orchestrator.statistics.mean_federate import MeanFederate
from scipy.stats import distributions


class LeveneFederate:
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
        mean_sample_0 = MeanFederate.Run(sample_0)
        mean_sample_1 = MeanFederate.Run(sample_1)

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
        pval = distributions.f.sf(f_statistic, 1, dof)  # 1 - cdf
        return f_statistic, pval
