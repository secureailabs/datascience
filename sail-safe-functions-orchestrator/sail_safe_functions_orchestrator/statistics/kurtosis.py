from scipy import stats

from .clients import kurtosis_agg_client, kurtosis_client


def kurtosis(
    clients,
    sample_0: list,
):
    list_list_precompute = []
    # TODO deal with posibilty sample_0 and sample_1 do net share same child frames

    # Calculating precompute
    for i in range(len(sample_0)):
        list_list_precompute.append(kurtosis_client(clients[i], sample_0[i]))

    # Final Kurtosis Value
    kurtosis_value = kurtosis_agg_client(clients[0], list_list_precompute)
    return kurtosis_value


def kurtosis_local(sample_0: list):
    return stats.kurtosis(sample_0)
