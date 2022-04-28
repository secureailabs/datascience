import pytest
import numpy as np
from scipy import stats

from sail_statstics.procedure.pearson.pearson_federate import PearsonFederate
from sail_statstics.local_federated_dataframe import LocalFederatedDataframe


@pytest.mark.active
def test_pearson():
    """
    This test our federated Skewness module

    """
    # Arrange
    sample_0 = LocalFederatedDataframe()
    sample_0_numpy = np.array([1, 2, 3, 4, 5, 6])
    sample_0.add_array("frame_test", "PD-L1 level before treatment", sample_0_numpy)
    sample_1 = LocalFederatedDataframe()
    sample_1_numpy = np.array([1, 2, 5, 6, 7, 4])
    sample_1.add_array("frame_test", "PD-L1 level before treatment", sample_1_numpy)
    # Calling fedrated sail Pearson method
    pearson_sail = PearsonFederate.pearson(sample_0, sample_1)
    print(pearson_sail)
    # Act
    pearson_scipy, p = stats.pearsonr(sample_0_numpy, sample_1_numpy)
    print(pearson_scipy)
    # Assert
    assert pearson_scipy == pytest.approx(pearson_sail, 0.0001)
