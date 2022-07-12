from typing import Tuple

import numpy
from sail_safe_functions.statistics.chisquare_agregate import ChisquareAgregate
from sail_safe_functions.statistics.chisquare_precompute import ChisquarePrecompute
from sail_safe_functions_orchestrator.series_federated import SeriesFederated
from sail_safe_functions_orchestrator.statistics.estimator import Estimator
from scipy.stats import chisquare


class Chisquare(Estimator):
    """
    Final function to run for Fedrated Chisquare test
    """

    @staticmethod
    def chisquare(sample_0: SeriesFederated, sample_1: SeriesFederated) -> Tuple[float, float]:
        """
        This test can be used to examine if there is a interaction between two paired categorical samples.

        The null hypothesis is that there is no interaction between samples.

        This test is invalid when the observed or expected frequencies in each category are too small.
        A typical rule is that all of the observed and expected frequencies should be at least 5.
        The total number of samples is recommended to be greater than 13.


        :param sample_0: Sample A
        :type sample_0: SeriesFederated
        :param sample_1: Sample B
        :type sample_1: SeriesFederated
        :return: returns the chisquare-statistic and the p-value
        :rtype: Tuple[float, float]
        """
        estimator = Chisquare()
        return estimator.run(sample_0, sample_1)

    def __init__(self) -> None:
        super().__init__(["chisquare_statistic", "p_value"])

    def run(self, sample_0: SeriesFederated, sample_1: SeriesFederated):

        # if not (is_string_dtype(sample_0) and is_string_dtype(sample_1)): TODO would be nice to catch this here
        #    raise ValueException()

        list_precompute = []
        for series_0, series_1 in zip(sample_0.dict_series.values(), sample_1.dict_series.values()):
            list_precompute.append(ChisquarePrecompute.run(series_0, series_1))
        return ChisquareAgregate.run(list_precompute)

    def run_reference(self, sample_0: SeriesFederated, sample_1: SeriesFederated):
        count_total = sample_0.size

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

        ddof = -((len(list_unique_0) - 1) * (len(list_unique_1) - 1)) + (
            len(array_true.ravel()) - 1
        )  # 2d instead of 1d
        chisquare_statistic, p_value = chisquare(array_true.ravel(), f_exp=array_pred.ravel(), ddof=ddof)
        return chisquare_statistic, p_value
