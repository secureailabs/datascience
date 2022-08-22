from typing import List


class KolmogorovSmirnovTestAggregate:
    """
    Aggregates data for the KolmogorovSmirnov test
    """

    def run(list_precompute: List[float]):
        """
        Calculate the aggregate Kolmogorov Smirnov Test

        :param list_precompute: list containing precomputes 
        :type list_precompute: List[float]
        :return: K-S test aggregate value
        :rtype: _type_
        """
        list_max = []
        for precompute in list_precompute:
            list_max.append(precompute)

        return max(list_max)
