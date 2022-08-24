from typing import Any, List

import pandas


class QueryPrecompute:
    def run(
        data_frame: pandas.DataFrame,
        query_expresion: str,
        parser: str,
        local_dict: dict,
        global_dict: dict,
    ) -> List:
        return data_frame.query(
            query_expresion,
            parser=parser,
            local_dict=local_dict,
            global_dict=global_dict,
        )
