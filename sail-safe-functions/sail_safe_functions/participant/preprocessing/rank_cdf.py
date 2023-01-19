from typing import List

import numpy
from sail_safe_functions.aggregator.data_model.data_model_series import DataModelSeries
from sail_safe_functions.aggregator.reference_series import ReferenceSeries
from sail_safe_functions.aggregator.series import Series
from sail_safe_functions.aggregator.service_reference import ServiceReference
from sail_safe_functions.safe_function_base import SafeFunctionBase
from scipy import interpolate


class RankCumulativeDistributionFunction(SafeFunctionBase):
    """
    Ranks the series using a given CDF of the full distribution
    """

    def run(
        series_0_reference: ReferenceSeries,
        size_sample_total: int,
        list_domain_cdf: List[float],
        list_value_cdf: List[float],
    ) -> ReferenceSeries:
        sample_0 = ServiceReference.get_instance().reference_to_series(series_0_reference)
        array_sample_0 = sample_0.to_numpy()
        function_cdf = interpolate.interp1d(numpy.array(list_domain_cdf), numpy.array(list_value_cdf))
        array_rank = numpy.round(function_cdf(array_sample_0) * size_sample_total)
        data_model_series = DataModelSeries.create_numerical(f"{sample_0.name}_ranked")
        series_ranked = Series(sample_0.dataset_id, data_model_series, array_rank.tolist())
        series_ranked_reference = ServiceReference.get_instance().series_to_reference(series_ranked)
        return series_ranked_reference
