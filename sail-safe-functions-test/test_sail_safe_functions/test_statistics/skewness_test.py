import pytest
import numpy as np
from scipy import stats

from sail_safe_functions_orchestrator.statistics.skewness_federate import SkewnessFederate

from helper_sail_safe_functions.series_federated_local import SeriesFederatedLocal

@pytest.mark.active
def test_skewness(one_sample_big):
    """
    This test our federated Skewness module


    Args:
        one_sample_big (SeriesFederatedLocal): A single federated series fixture
    """
    # Arrange
    sample_0 = one_sample_big

    # Act
    # Calling fedrated sail skewness method
    skewness_sail = SkewnessFederate.skewness(sample_0)
    skewness_scipy = stats.skew(sample_0.to_numpy())

    # Assert
    assert skewness_scipy == pytest.approx(skewness_sail, 0.0001)
