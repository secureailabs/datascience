from typing import Tuple

import numpy
import pandas
from sail_safe_functions.aggregator.reference_series import ReferenceSeries
from sail_safe_functions.aggregator.service_reference import ServiceReference
from sail_safe_functions.aggregator.tools_common import (
    check_empty_series,
    check_series_constant,
    check_series_nan,
    check_series_one_value,
)
from sail_safe_functions.safe_function_base import SafeFunctionBase


class WilcoxonSingedRankTestPrecompute(SafeFunctionBase):
    """
    Precomputes data for the  WilcoxonSingedRankTest
    """

    @staticmethod
    def run(
        reference_sample_difference: ReferenceSeries,
        reference_sample_absolute_difference_ranked: ReferenceSeries,
    ) -> Tuple[float, float]:
        """
        Function to Precomputes data for the  WilcoxonSingedRankTest TODO: What does this mean? Be more verbose than the function name.

        :param reference_sample_difference: reference to the sample input
        :type sample_difference: ReferenceSeries
        :param reference_sample_absolute_difference_ranked: absolute differences ranked TODO: what does this mean? Be more verbose than the variable name.
        :type sample_absolute_difference_ranked: ReferenceSeries
        :return: Tuple rank_minus, rank_plus TODO: What does this mean?
        :rtype: Tuple[float, float]
        """
        sample_difference = ServiceReference.get_instance().reference_to_series(reference_sample_difference).to_numpy()
        sample_absolute_difference_ranked = (
            ServiceReference.get_instance().reference_to_series(reference_sample_absolute_difference_ranked).to_numpy()
        )
        check_series_nan(sample_difference)
        check_series_nan(sample_absolute_difference_ranked)
        # check_series_one_value(sample_difference) TODO move these
        # check_series_one_value(sample_absolute_difference_ranked)

        # check_series_constant(sample_difference)  TODO move these
        # check_series_constant(sample_absolute_difference_ranked)

        rank_minus = numpy.sum((sample_difference < 0) * sample_absolute_difference_ranked)
        rank_plus = numpy.sum((sample_difference > 0) * sample_absolute_difference_ranked)
        return [rank_minus, rank_plus]
