from typing import List, Tuple


class MinMaxAgregate:
    """
    Agregates min and max for a given sample
    """

    def run(list_tuple_min_max: List[Tuple[float, float]]) -> Tuple[float, float]:
        """Agregates the results of multiple precompute functions into a global min and max

        :param list_tuple_min_max: A list of tuples from various precompute functions
        :type list_tuple_min_max: List[Tuple[float, float]]
        :return: return the federated estimated sample min max
        :rtype: Tuple[float, float]
        """
        list_min = []
        list_max = []
        for tuple_min_max in list_tuple_min_max:
            list_min.append(tuple_min_max[0])
            list_max.append(tuple_min_max[1])
        return min(list_min), max(list_max)
