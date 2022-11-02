import numpy
from pandas import Series
from sail_safe_functions.preprocessing.rank_cdf import (
    RankCumulativeDistributionFunction,
)
from sail_safe_functions_orchestrator import preprocessing
from sail_safe_functions_orchestrator.series_federated import SeriesFederated
from sail_safe_functions_orchestrator.tools_common import check_instance
from scipy.stats import rankdata


def rank_unsafe(sample_0: SeriesFederated) -> SeriesFederated:
    """
    :param sample_0: Input sample series
    :type sample_0: SeriesFederated
    :return: ranked sample
    :rtype: SeriesFederated
    """
    check_instance(sample_0, SeriesFederated)
    list_size = []
    list_array = []
    for series in sample_0.dict_series.values():
        list_size.append(series.size)
        list_array.append(series.to_numpy())
    array_sample = numpy.concatenate(list_array)
    array_rank = rankdata(array_sample)

    sample_ranked_0 = sample_0.create_new()
    index_start = 0
    for i, dataset_id in enumerate(sample_0.dict_series):
        index_end = index_start + list_size[i]
        sample_ranked_0.add_array(
            dataset_id,
            Series(array_rank[index_start:index_end], name=f"{sample_0.name}_ranked"),
        )
        index_start = index_end
    return sample_ranked_0


def rank_cdf(sample_0: SeriesFederated) -> SeriesFederated:
    check_instance(sample_0, SeriesFederated)
    list_domain_cdf, list_value_cdf = preprocessing.cdf(sample_0)
    sample_ranked_0 = sample_0.create_new()
    for dataset_id, series in sample_0.dict_series.items():  # TODO rework abcs
        sample_ranked_0.add_series(
            dataset_id,
            RankCumulativeDistributionFunction.run(series, len(sample_0.to_numpy()), list_domain_cdf, list_value_cdf),
        )
    return sample_ranked_0


def rank(sample_0: SeriesFederated, type_ranking: str) -> SeriesFederated:
    check_instance(sample_0, SeriesFederated)
    check_instance(type_ranking, str)
    """Ranks series in a federated with, ideally with minimal data leaving the contribution

    :param sample_0: The sample to be ranked
    :type sample_0: SeriesFederated
    :param mode: the mode in which to use the algoritm,  `unsafe` should never end in production
    :type mode: str
    :raises ValueError: ValueError: raise a ValueError of mode is not `unsafe` or `cdf`
    :return: A federated series that has been converted into ranks
    :rtype: SeriesFederated
    """
    if type_ranking not in {"unsafe", "cdf"}:
        raise ValueError("mode must be `unsafe`, `cdf`")
    if type_ranking == "unsafe":
        return rank_unsafe(sample_0)
    elif type_ranking == "cdf":
        return rank_cdf(sample_0)
    else:
        raise ValueError("mode must be `unsafe`, `cdf`")
