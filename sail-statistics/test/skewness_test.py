import pytest
import numpy as np
from scipy import stats

from sail_statstics.procedure.skewness.skewness_federate import SkewnessFederate
from sail_statstics.local_federated_dataframe import LocalFederatedDataframe


@pytest.mark.active
def test_skewness():
    """
    This test our federated Skewness module
    """

    sample_0 = LocalFederatedDataframe()
    sample_0_numpy = np.array([17.2, 20.9, 22.6, 18.1, 21.7, 21.4, 23.5, 24.2, 14.7, 21.8])
    sample_0.add_array("frame_test", "PD-L1 level before treatment", sample_0_numpy)
    skewness_sail = SkewnessFederate.skewness_ind(sample_0)
    # skewness_sail=0

    skewness_scipy = stats.skew(sample_0_numpy)
    print(skewness_scipy)
    skewness_mean = skewness_scipy

    # Assert
    assert skewness_scipy == pytest.approx(skewness_sail, 0.0001)
