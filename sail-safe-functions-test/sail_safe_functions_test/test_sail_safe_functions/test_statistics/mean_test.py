import numpy as np
import pytest
from sail_safe_functions_orchestrator import statistics
from sail_safe_functions_orchestrator.statistics.mean import Mean
from sail_safe_functions_test.helper_sail_safe_functions.series_federated_local import SeriesFederatedLocal


@pytest.mark.active
def test_mean_direct(one_sample_big: SeriesFederatedLocal):
    statistics.mean(one_sample_big)


@pytest.mark.active
def test_mean(one_sample_big: SeriesFederatedLocal):
    """A test of the mean value statisc

    Args:
        one_sample_big (SeriesFederatedLocal): A single federated series fixture
    """
    # Arrange
    sample_0 = one_sample_big

    # Act
    estimator = Mean()
    mean_sail = estimator.Run(sample_0)
    mean_numpy = estimator.run_reference(sample_0)

    # Assert
    assert mean_sail == pytest.approx(mean_numpy, 0.0001)
