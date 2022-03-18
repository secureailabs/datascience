from typing import Any, List, Tuple

import numpy as np

from sail_statstics.procedure.safe_function import SafeFunction

class TTestPrecompute(SafeFunction):
    
    def __init__(self) -> None:
        super().__init__()

    
    def run(
        sample_0:np.ndarray, 
        sample_1:np.ndarray) -> Tuple[List[float], List[bool]]: # there seems to be a problem here with this annotation
    
        sum_x_0 = np.sum(sample_0) 
        sum_xx_0 = np.sum(sample_0 * sample_0) 
        sample_0_dof = len(sample_0)
        
        sum_x_1 = np.sum(sample_1) 
        sum_xx_1 = np.sum(sample_1 * sample_1) 
        sample_1_dof = len(sample_1)
        
        list_precompute = [sum_x_0, sum_xx_0, sample_0_dof, sum_x_1, sum_xx_1, sample_1_dof]
        # list_safe = [False, False, False, False, False, False ]
        return list_precompute#, list_safe