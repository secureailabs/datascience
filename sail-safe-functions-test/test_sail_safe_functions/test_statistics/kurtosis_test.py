import pytest
import numpy as np
from scipy import stats

from sail_safe_functions_orchestrator.statistics.kurtosis_federate import KurtosisFederate

from helper_sail_safe_functions.series_federated_local import SeriesFederatedLocal

@pytest.mark.active
def test_kurtosis(one_sample_big: SeriesFederatedLocal):
    """
    This test our federated kurtosis module

    Args:
        one_sample_big (SeriesFederatedLocal): A single federated series fixture
    """
    # Arrange
    sample_0 = one_sample_big

    # Act
    kurtosis_sail = KurtosisFederate.kurtosis(sample_0)
    kurtosis_scipy = stats.kurtosis(sample_0.to_numpy())

    # Assert
    assert kurtosis_scipy == pytest.approx(kurtosis_sail, 0.0001)
