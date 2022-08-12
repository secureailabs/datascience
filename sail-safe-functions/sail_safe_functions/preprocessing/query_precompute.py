from typing import Any, List

import pandas


class QueryPrecompute:
    def run(data_frame: pandas.DataFrame, query_expresion: Any) -> List:
        return data_frame.query(query_expresion)
