from collections import Counter
from typing import List


class HistogramAggregate:
    """
    Aggregates the final list for the histogrm.
    """

    # list of precompute contains list of list
    # example list_list_precompute = [ [L1,L2], [L3,L4], [L5, L6] ]
    # L1 -> Unique value for the 1st series.
    # L2 -> Frequency of unique value for the 1st series.
    # L3 -> Unique value for the 2nd series.
    # L4 -> Frequency of unique value for the 2nd series.
    # And so on and on

    @staticmethod
    def run(list_list_precompute: List[List[List[float]]]):
        """
        Function get the aggregated list value counts

        :param list_list_precompute: list
        :type list_list_precompute: List[List[float]]
        :return: values for histogram
        :rtype: value
        """
        print(list_list_precompute)
        final = {}
        for list_precompute in list_list_precompute:
            # initialising dictionaries
            final = Counter(final)
            L1 = list_precompute[0]
            L2 = list_precompute[1]
            ini_dictionary2 = {L1[i]: L2[i] for i in range(len(L1))}
            ini_dictionary2 = Counter(ini_dictionary2)
            # combining dictionaries
            # using Counter
            final = final + ini_dictionary2

        final_list = []
        for key in final:
            for i in range(final[key]):
                final_list.append(key)

        return final_list
