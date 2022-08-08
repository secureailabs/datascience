from typing import List

import numpy


class MannWhitneyUTestAggregate:
    """
    The aggregate function of the mann withnet u test
    """

    def run(list_precompute: List[float]) -> float:
        """
        The aggregate function of the mann withnet u test

        :param list_precompute: _description_
        :type list_precompute: List[float]
        :return: _description_
        :rtype: float
        """
        return numpy.array(list_precompute).sum()
