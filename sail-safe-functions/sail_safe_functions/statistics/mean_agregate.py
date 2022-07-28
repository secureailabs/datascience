from typing import List


class MeanAggregate:
    """
    Aggregates data for computing the mean
    """

    def Run(list_list_precompute: List[List[float]]):
        sum_x_0 = 0
        degrees_of_freedom_0 = 0

        for list_precompute in list_list_precompute:
            sum_x_0 += list_precompute[0]
            degrees_of_freedom_0 += list_precompute[1]

        sample_mean_0 = sum_x_0 / degrees_of_freedom_0

        # if degrees_of_freedom < 20:
        #     raise Exception()
        return sample_mean_0
