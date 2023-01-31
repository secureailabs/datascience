from typing import Dict, Tuple

import numpy
from sail_core.implementation_manager import ImplementationManager
from sail_safe_functions.aggregator.series_federated import SeriesFederated
from sail_safe_functions.aggregator.statistics.estimator_two_sample import EstimatorTwoSample
from sail_safe_functions.participant.statistics.chisquare_precompute import ChisquarePrecompute
from scipy import stats
from scipy.stats import distributions


def chisquare(sample_0: SeriesFederated, sample_1: SeriesFederated) -> Tuple[float, float]:
    """
    Perform federated chisquare test.
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


class Chisquare(EstimatorTwoSample):
    """
    Final function to run for Fedrated Chisquare test
    """

    def __init__(self) -> None:
        super().__init__("ChisquareTest for independance", ["chisquare_statistic", "p_value"])

    def run(self, sample_0: SeriesFederated, sample_1: SeriesFederated) -> Tuple[float, float]:

        list_precompute = []
        for dataset_id in sample_0.list_dataset_id:
            participant_service = ImplementationManager.get_instance().get_participant_service()
            precompute = participant_service.call(
                dataset_id,
                ChisquarePrecompute,
                sample_0.dict_reference_series[dataset_id],
                sample_1.dict_reference_series[dataset_id],
            )
            list_precompute.append(precompute)
        return self.aggregate(list_precompute)

    def aggregate(self, list_precompute) -> Tuple[float, float]:

        list_unique_0 = []
        list_unique_1 = []
        for precompute in list_precompute:
            for tuple_value in precompute:
                value_0 = tuple_value[0]
                value_1 = tuple_value[1]
                if value_0 not in list_unique_0:
                    list_unique_0.append(value_0)
                if value_1 not in list_unique_1:
                    list_unique_1.append(value_1)

        array_true = numpy.zeros((len(list_unique_0), len(list_unique_1)))
        array_pred = numpy.zeros((len(list_unique_0), len(list_unique_1)))
        count_total = 0
        for precompute in list_precompute:
            for tuple_value in precompute:
                value_0 = tuple_value[0]
                value_1 = tuple_value[1]
                index_0 = list_unique_0.index(value_0)
                index_1 = list_unique_1.index(value_1)
                array_true[index_0, index_1] += precompute[tuple_value]
                count_total += precompute[tuple_value]

        for i_0 in range(array_true.shape[0]):
            for i_1 in range(array_true.shape[1]):
                array_pred[i_0, i_1] = array_true[i_0, :].sum() * array_true[:, i_1].sum() / count_total

        array_true = array_true.ravel()
        array_pred = array_pred.ravel()
        chisquare_statistic = (numpy.power(array_true - array_pred, 2) / array_pred).sum()
        degrees_of_freedom = (len(list_unique_0) - 1) * (len(list_unique_1) - 1)

        p_value = float(distributions.chi2.sf(chisquare_statistic, degrees_of_freedom))
        return chisquare_statistic, p_value
