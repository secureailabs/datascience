from typing import List


class VarianceAggregate:
    """
    Aggregates data for computing the Variance
    """

    def run(list_list_precompute: List[List[float]]):
        """
        This method to run aggregated variance

            :param list_list_precompute: list of precomputes
            :type list_list_precompute: List[List[float]]
            :return: Variance Value
            :rtype: Float
        """
        sum_x_0 = 0
        sum_xx_0 = 0
        size_sample_0 = 0

        for list_precompute in list_list_precompute:
            sum_x_0 += list_precompute[0]
            sum_xx_0 += list_precompute[1]
            size_sample_0 += list_precompute[2]

        sample_mean_0 = sum_x_0 / size_sample_0

        sample_variance_0 = ((sum_xx_0 / size_sample_0) - (sample_mean_0 * sample_mean_0)) * (
            size_sample_0 / (size_sample_0 - 1)  # unbiased estimator (numpy version is biased by default)
        )

        return sample_variance_0
