from typing import Any, List, Tuple

import numpy as np

from sail_statstics.procedure.safe_function import SafeFunction

class TTest(SafeFunction):
    
    def __init__(self) -> None:
        super().__init__()

    
    def compute(
        list_remote_data_frame:List[str],
        querry:str,
        id_column:str, 
        list_remote_data_frame:List[str],
        querry:str,
        id_column:str, 
        sample_1:str) -> Tuple[List[float], List[bool]]: # there seems to be a problem here with this annotation

        return list_precompute#, list_safe

        compute_graph = []