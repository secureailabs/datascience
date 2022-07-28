import math
from typing import List


class KolmogorovSmirnovTestAggregate:
    """
    Aggregates data for the KolmogorovSmirnov test
    """

    def run(list_precompute: List[float]):
        list_max = []
        for precompute in list_precompute:
            list_max.append(precompute)

        return max(list_max)
