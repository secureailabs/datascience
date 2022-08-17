from typing import Any, Dict

from sail_safe_functions.preprocessing.query_precompute import apPrecompute
from sail_safe_functions_orchestrator.series_federated import SeriesFederated
from sail_safe_functions_orchestrator.tools_common import check_instance


def map(data_frame_source: SeriesFederated, query_expresion: Any) -> SeriesFederated:
    return Map.run(data_frame_source, query_expresion)


class Map:
    """
    Drop rows or columns with missing data
    """

    def run(series_source: SeriesFederated, map: Dict[str, str]) -> SeriesFederated:

        check_instance(series_source, SeriesFederated)
        # check_instance(query_expresion, list) #TODO
        series_target = series_source.create_new()
        # TODO check
        for dataset_id in series_source.dict_series:
            series_target.dict_series[dataset_id] = MapPrecompute.run(series_source.dict_series[dataset_id], map)
        return series_target
