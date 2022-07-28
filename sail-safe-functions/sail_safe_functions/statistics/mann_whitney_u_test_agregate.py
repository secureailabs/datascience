from typing import List

import numpy


class MannWhitneyUTestAggregate:
    """
    The agregate function of the mann withnet u test
    """

    def run(list_precompute: List[float]) -> float:
        return numpy.array(list_precompute).sum()
