from typing import List

import numpy


class MannWhitneyUTestAggregate:
    """
    The aggregate function of the mann withnet u test
    """

    def run(list_precompute: List[float]) -> float:
        """
        The aggregate function of the mann withnet u test

            :param list_precompute: list of precompute
            :type list_precompute: List[float]
            :return: Aggregate value for mann whitney u test
            :rtype: float
        """
        return numpy.array(list_precompute).sum()
