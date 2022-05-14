import pandas
from sail_safe_functions.statistics.pearson_agregate import PearsonAgregate
from sail_safe_functions.statistics.pearson_precompute import PearsonPrecompute
from sail_safe_functions_orchestrator.series_federated import SeriesFederated
from scipy.stats import rankdata


class RankFederate:
    @staticmethod
    def run_unsafe(sample_0: SeriesFederated) -> SeriesFederated:
        
        
        list_size = []
        list_array = []
        for federation_contribution_id, series in sample_0.items():
            list_size.append(series.lenght)
            list_array
        array_sample
        array_rank  = rankdata(array_sample)

        rank_0 = SeriesFederated()
        for federation_contribution_id, series in sample_0.items(): 
        pandas.Series([], name=name)
            rank_0.add_array()
        return rank_0

    @staticmethod
    def run_cdf(sample_0: SeriesFederated) -> SeriesFederated:
        

        return sample_0

    @staticmethod
    def run(sample_0: SeriesFederated, mode: str) -> SeriesFederated:

        if mode not in {"unsafe", "cdf"}:
            raise ValueError("mode must be `unsafe`, `cdf`")
        if mode == "unsafe":
            return RankFederate.run_unsafe(sample_0)
        elif mode == "unsafe":
            return RankFederate.run_cdf(sample_0)
        else:
            raise ValueError("mode must be `unsafe`, `cdf`")


