import numpy
from sail_core.implementation_manager import ImplementationManager
from sail_core.tools_common import check_instance
from sail_safe_functions.aggregator import preprocessing, statistics
from sail_safe_functions.aggregator.data_model.data_model_series import DataModelSeries
from sail_safe_functions.aggregator.series import Series
from sail_safe_functions.aggregator.series_federated import SeriesFederated
from sail_safe_functions.aggregator.service_reference import ServiceReference
from sail_safe_functions.participant.preprocessing.rank_cdf import RankCumulativeDistributionFunction
from scipy.stats import rankdata


def rank_unsafe(sample_0: SeriesFederated) -> SeriesFederated:
    check_instance(sample_0, SeriesFederated)
    list_size = []
    list_array = []
    for reference in sample_0.dict_reference_series.values():
        series = ServiceReference.get_instance().reference_to_series(reference)
        list_size.append(series.size)
        list_array.append(series.to_numpy())
    array_sample = numpy.concatenate(list_array)
    array_rank = rankdata(array_sample)

    series_name = sample_0.series_name + "_ranked"
    data_model_series = DataModelSeries.create_numerical(series_name, -1, None, DataModelSeries.AgregatorComputed)

    index_start = 0
    list_reference = []
    for i, dataset_id in enumerate(sample_0.list_dataset_id):
        index_end = index_start + list_size[i]
        series = Series(dataset_id, data_model_series, array_rank[index_start:index_end].tolist())
        reference = ServiceReference.get_instance().series_to_reference(series)
        list_reference.append(reference)
        index_start = index_end

    return SeriesFederated(list_reference, data_model_series)


def rank_cdf(sample_0: SeriesFederated) -> SeriesFederated:
    check_instance(sample_0, SeriesFederated)
    list_domain_cdf, list_value_cdf = preprocessing.cumulative_distribution_function(sample_0)
    list_reference = []
    count = statistics.count(sample_0)
    service_participant = ImplementationManager.get_instance().get_participant_service()
    for dataset_id in sample_0.list_dataset_id:
        reference_series_0 = sample_0.get_reference_series(dataset_id)
        reference_series_0_ranked = service_participant.call(
            dataset_id, RankCumulativeDistributionFunction, reference_series_0, count, list_domain_cdf, list_value_cdf
        )
        list_reference.append(reference_series_0_ranked)
    return SeriesFederated(list_reference, reference_series_0.data_model_series)


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
