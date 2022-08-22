from xmlrpc.client import Boolean
import numpy as np
import pandas


class kl_divergence:
    """
    KL divergence class to run kl divergence on two sample
    """

    def kl_divergence(self, a: pandas.Series, b: pandas.Series):
        """
        it take two sample and returns kl divegrence between the distribution

            :param a: First sample distribution
            :type a: pandas.series
            :param b: Second sample disitribution
            :type b: pandas.series
            :return: kl divergence between two distribution
            :rtype: float
        """
        return sum(a[i] * np.log(a[i] / b[i]) for i in range(len(a)))

    def run(self, sample_0: pandas.Series, sample_1: pandas.Series, reverse: Boolean):
        """
        kl divergence between same distribtion could be different for two same distribution
        There are two ways do tha Kl divergence. Forward kl and Reverse kl

            :param sample_0: first input distibution
            :type sample_0: pandas.Series
            :param sample_1: Second input distribution
            :type sample_1: pandas.Series
            :param reverse: If reverse is True it will run Reverse KL
            :type reverse: Boolean
            :return: kl divergence between two distribution
            :rtype: Float
        """
        # Reverse KL
        if reverse:
            value = self.kl_divergence(sample_1, sample_0)
        # Forward KL
        else:
            value = self.kl_divergence(sample_0, sample_1)

        return value
