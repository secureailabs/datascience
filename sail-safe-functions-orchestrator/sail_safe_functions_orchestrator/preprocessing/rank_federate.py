import numpy
from pandas import Series
from sail_safe_functions.preprocessing.rank_cdf import RankCdf
from sail_safe_functions_orchestrator.preprocessing.cdf_federate import CdfFederate
from sail_safe_functions_orchestrator.series_federated import SeriesFederated
from sail_safe_functions_test.helper_sail_safe_functions.series_federated_local import SeriesFederatedLocal
from scipy.stats import rankdata


class RankFederate:
    @staticmethod
    def run_unsafe(sample_0: SeriesFederated) -> SeriesFederated:

        list_size = []
        list_array = []
        for federation_contribution_id, series in sample_0.dict_series.items():
            list_size.append(series.size)
            list_array.append(series.to_numpy())
        array_sample = numpy.concatenate(list_array)
        array_rank = rankdata(array_sample)

        sample_ranked_0 = SeriesFederatedLocal()
        index_start = 0
        for i, federation_contribution_id in enumerate(sample_0.dict_series):
            index_end = index_start + list_size[i]
            sample_ranked_0.add_array(
                federation_contribution_id, Series(array_rank[index_start:index_end], name=f"{sample_0.name}_ranked")
            )
            index_start = index_end
        return sample_ranked_0

    @staticmethod
    def run_cdf(sample_0: SeriesFederated) -> SeriesFederated:

        list_domain_cdf, list_value_cdf = CdfFederate.run(sample_0)
        sample_ranked_0 = SeriesFederatedLocal()  # TODO become more clever  as this is basically a synthetic field
        for federation_contribution_id, series in sample_0.dict_series.items():  # TODO rework abcs
            sample_ranked_0.add_series(
                federation_contribution_id,
                RankCdf.run(series, len(sample_0.to_numpy()), list_domain_cdf, list_value_cdf),
            )
        return sample_ranked_0

    @staticmethod
    def run(sample_0: SeriesFederated, mode: str) -> SeriesFederated:

        if mode not in {"unsafe", "cdf"}:
            raise ValueError("mode must be `unsafe`, `cdf`")
        if mode == "unsafe":
            return RankFederate.run_unsafe(sample_0)
        elif mode == "cdf":
            return RankFederate.run_cdf(sample_0)
        else:
            raise ValueError("mode must be `unsafe`, `cdf`")
