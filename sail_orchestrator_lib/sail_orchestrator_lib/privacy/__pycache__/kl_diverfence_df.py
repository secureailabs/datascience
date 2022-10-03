from xmlrpc.client import Boolean
import numpy as np
import pandas


class kl_divergence_df:
    """
    KL divergence class to run kl divergence on two sample dataframes
    """

    def kl_divergence_df(self, a: pandas.DataFrame, b: pandas.DataFrame):
        """
        it take two dataframe samples and returns kl divegrence between them.
            :param a: First sample distribution
            :type a: pandas.DataFrame
            :param b: Second sample disitribution
            :type b: pandas.DataFrame
            :return: kl divergence between two distribution
            :rtype: float
        """
        # First convert to np array
        P = np.array(a)
        Q = np.array(b)

        # Then compute their means
        mu_P = np.mean(P, axis=0)
        mu_Q = np.mean(Q, axis=0)

        # Compute their covariance
        cov_P = np.cov(P, rowvar=False)
        cov_Q = np.cov(Q, rowvar=False)

        cov_Q_inv = np.linalg.inv(cov_Q)

        # Compute KL divergence
        KL_div = (
            np.log(np.linalg.det(cov_Q) / np.linalg.det(cov_P))
            - mu_P.shape[0]
            + np.trace(cov_Q_inv @ cov_P)
            + (mu_P - mu_Q).T @ cov_Q_inv @ (mu_P - mu_Q)
        )

        KL_div = 0.5 * KL_div

        return KL_div

    def run(self, sample_0: pandas.DataFrame, sample_1: pandas.DataFrame, reverse: Boolean):
        """
        kl divergence between same distribtion could be different for two same distribution
        There are two ways do tha Kl divergence. Forward kl and Reverse kl
            :param sample_0: first input distibution
            :type sample_0: pandas.DataFrame
            :param sample_1: Second input distribution
            :type sample_1: pandas.DataFrame
            :param reverse: If reverse is True it will run Reverse KL
            :type reverse: Boolean
            :return: kl divergence between two distribution
            :rtype: Float
        """
        # Reverse KL
        if reverse:
            value = self.kl_divergence_df(sample_1, sample_0)
        # Forward KL
        else:
            value = self.kl_divergence_df(sample_0, sample_1)

        return value
