from sail_core.tools_common import check_instance
from sail_safe_functions.aggregator.reference_series import ReferenceSeries
from sail_safe_functions.aggregator.service_reference import ServiceReference
from sail_safe_functions.aggregator.tools_common import check_empty_series, check_series_nan, check_series_one_value
from sail_safe_functions.safe_function_base import SafeFunctionBase


class MannWhitneyUTestPrecompute(SafeFunctionBase):

    """
    The precompute function of the mann withnet u test
    """

    def run(reference_series_0: ReferenceSeries, reference_series_concatenated_ranked: ReferenceSeries) -> float:
        """
        precompute function of the mann withnet u test

            :param reference_series_0: Input sample
            :type reference_series_0: ReferenceSeries
            :param reference_series_concatenated_ranked: Concatenated ranked series TODO: What does this mean? Please be more verbose than the variable name.
            :type reference_series_concatenated_ranked: ReferenceSeries
            :return: _description_ TODO: what does this mean?
            :rtype: float
        """

        series_0 = ServiceReference.get_instance().reference_to_series(reference_series_0).to_numpy()
        series_concatenated_ranked = (
            ServiceReference.get_instance().reference_to_series(reference_series_concatenated_ranked).to_numpy()
        )
        check_empty_series(series_0)
        check_series_nan(series_0)

        # check_series_one_value(series_0) TODO move these up and only one
        # check_series_one_value(series_concatenated_ranked)

        return series_concatenated_ranked[: series_0.size].sum()
