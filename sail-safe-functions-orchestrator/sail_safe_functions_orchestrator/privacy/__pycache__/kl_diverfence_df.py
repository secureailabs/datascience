import numpy as np
import pandas


def kl_divergence_df(
    a: pandas.DataFrame,
    b: pandas.DataFrame,
    reverse: bool,
):
    """
    it take two dataframe samples and returns kl divegrence between them.
        :param a: First sample distribution
        :type a: pandas.DataFrame
        :param b: Second sample disitribution
        :type b: pandas.DataFrame
        :return: kl divergence between two distribution
        :rtype: float
    """
    if reverse:
        a, b = b, a

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
