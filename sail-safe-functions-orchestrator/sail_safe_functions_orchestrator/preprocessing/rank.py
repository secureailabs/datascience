import numpy
from sail_safe_functions.preprocessing.rank_cdf import RankCumulativeDistributionFunction
from sail_safe_functions_orchestrator import preprocessing
from sail_safe_functions_orchestrator.data_model.data_model_series import DataModelSeries
from sail_safe_functions_orchestrator.series import Series
from sail_safe_functions_orchestrator.series_federated import SeriesFederated
from sail_safe_functions_orchestrator.service_reference import ServiceReference
from sail_safe_functions_orchestrator.tools_common import check_instance
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
    for i, dataset_id in enumerate(sample_0.dict_reference_series):
        index_end = index_start + list_size[i]
        series = Series(dataset_id, data_model_series, array_rank[index_start:index_end].tolist())
        reference = ServiceReference.get_instance().series_to_reference(series)
        list_reference.append(reference)
        index_start = index_end

    return SeriesFederated(sample_0.service_client, list_reference, data_model_series)


def rank_cdf(sample_0: SeriesFederated) -> SeriesFederated:
    check_instance(sample_0, SeriesFederated)
    list_domain_cdf, list_value_cdf = preprocessing.CumulativeDistributionFunction(sample_0)
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
