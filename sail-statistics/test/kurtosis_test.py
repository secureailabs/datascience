import pytest
import numpy as np
from scipy import stats

from sail_statstics.procedure.kurtosis.kurtosis_federate import KurtosisFederate
from sail_statstics.local_federated_dataframe import LocalFederatedDataframe


@pytest.mark.active
def test_kurtosis():
    """
    This test our federated Skewness module

    """
    # Arrange
    sample_0 = LocalFederatedDataframe()
    sample_0_numpy = np.array([17.2, 20.9, 22.6, 18.1, 21.7, 21.4, 23.5, 24.2, 14.7, 21.8])
    sample_0.add_array("frame_test", "PD-L1 level before treatment", sample_0_numpy)
    # Calling fedrated sail kurtosis method
    kurtosis_sail = KurtosisFederate.kurtosis_ind(sample_0)

    # Act
    kurtosis_scipy = stats.kurtosis(sample_0_numpy)
    print(kurtosis_scipy)
    print(kurtosis_sail)
    # Assert
    assert kurtosis_scipy == pytest.approx(kurtosis_sail, 0.0001)
