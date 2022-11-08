from typing import List

import numpy
from pandas import Series
from sail_safe_functions_orchestrator.reference_series import ReferenceSeries
from sail_safe_functions_orchestrator.service_reference import ServiceReference
from scipy import stats
from sail_safe_functions_orchestrator.tools_common import (
    check_instance,
    check_series_nan,
    check_empty_series,
    check_series_one_value,
)


class KolmogorovSmirnovTestPrecompute:
    """
    Precomputes data for the KolmogorovSmirnov test
    """

    def run(
        refrence_sample_0: ReferenceSeries,
        refrence_sample_0_ranked: ReferenceSeries,
        distribution: str,
        count_total: int,
    ) -> List[float]:
        """
        Calculate the preceomputes for KolmogorovSmirnov test

            :param refrence_sample_0: First input sample
            :type refrence_sample_0: ReferenceSeries
            :param refrence_sample_0_ranked: Second input sample TODO: I don't think this is accurate.
            :type refrence_sample_0_ranked: ReferenceSeries
            :param distribution: Type of distribution ypu want to have TODO: what does this mean?
            :type distribution: str
            :param count_total: total count TODO: this needs to be more informative
            :type count_total: int
            :return: KS Test precompute
            :rtype: List[float] TODO: why are some return types of stat functions lists, whereas others are Dicts?
        """

        type_distribution = distribution["type_distribution"]

        array_sample_0 = ServiceReference.get_instance().reference_to_series(refrence_sample_0).to_numpy()
        array_sample_ranked_0 = ServiceReference.get_instance().reference_to_series(refrence_sample_0_ranked).to_numpy()
        check_empty_series(array_sample_0)
        check_empty_series(array_sample_ranked_0)

        if type_distribution == "normal":
            sample_mean = numpy.mean(array_sample_0)
            sample_sdev = numpy.std(array_sample_0, ddof=1)
            array_value_cdf = stats.norm.cdf(array_sample_0, loc=sample_mean, scale=sample_sdev)
        elif type_distribution == "normalunit":
            array_value_cdf = stats.norm.cdf(array_sample_0, loc=0, scale=1)
        else:
            raise Exception()
        return numpy.max(numpy.abs((array_sample_ranked_0 / count_total) - array_value_cdf))
