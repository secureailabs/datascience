from typing import List

import numpy
from sail_safe_functions.safe_function_base import SafeFunctionBase


class MannWhitneyUTestAggregate(SafeFunctionBase):

    """
    The aggregate function of the mann withnet u test
    """

    def run(list_precompute: List[float]) -> float:
        return numpy.array(list_precompute).sum()
