from typing import Dict

import numpy
from scipy.stats import distributions


class ChisquareAggregate:
    """
    Aggregates data for Chisquare test
    """

    def run(list_precompute) -> Dict:

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
                array_pred[i_0, i_1] = (
                    array_true[i_0, :].sum() * array_true[:, i_1].sum() / count_total
                )

        array_true = array_true.ravel()
        array_pred = array_pred.ravel()
        chisquare_statistic = (
            numpy.power(array_true - array_pred, 2) / array_pred
        ).sum()
        degrees_of_freedom = (len(list_unique_0) - 1) * (len(list_unique_1) - 1)

        p_value = distributions.chi2.sf(chisquare_statistic, degrees_of_freedom)
        return chisquare_statistic, p_value
