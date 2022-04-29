import numpy as np
import pytest
from sail_safe_functions_orchestrator.statistics.mean_federate import \
    MeanFederate
from sail_safe_functions_test.helper_sail_safe_functions.series_federated_local import \
    SeriesFederatedLocal


@pytest.mark.active
def test_mean(one_sample_big: SeriesFederatedLocal):
    """A test of the mean value statisc

    Args:
        one_sample_big (SeriesFederatedLocal): A single federated series fixture
    """
    # Arrange
    sample_0 = one_sample_big

    # Act
    mean_sail = MeanFederate.mean(sample_0)
    mean_numpy = np.mean(sample_0.to_numpy())

    # Assert
    assert mean_sail == pytest.approx(mean_numpy, 0.0001)
