from typing import List

import pandas


class ExpresionPrecompute:
    def run(
        data_frame_source: pandas.DataFrame, name_feature_source: str, name_feature_target: str, expresion_string: str
    ):
        data_frame_target = data_frame_source.copy()
        data_frame_target[name_feature_target] = data_frame_source[name_feature_source].map(expresion_string)
        return data_frame_target
