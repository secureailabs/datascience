import numpy as np
import pytest
from sail_safe_functions_orchestrator import statistics
from sail_safe_functions_orchestrator.statistics.mean import Mean
from sail_safe_functions_test.helper_sail_safe_functions.series_federated_local import (
    SeriesFederatedLocal,
)
import numpy


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
    mean_sail = estimator.run(sample_0)
    mean_numpy = estimator.run_reference(sample_0)

    # Assert
    assert mean_sail == pytest.approx(mean_numpy, 0.0001)


@pytest.mark.active
def test_mean_empty():
    """
    This is our test to raise exception for empty
    """
    # Arrange
    numpy.random.seed(42)
    sample_size = 0
    sample_0 = SeriesFederatedLocal.from_array("dataset_0", "series_0", numpy.random.normal(0, 1, sample_size))
    # Act
    estimator = Mean()

    with pytest.raises(Exception) as exc_info:
        #   pearson_sail, p_value_sail = estimator.run(sample_0, sample_1)
        estimator.run(sample_0)

    # Assert
    assert "series cannot be empty" == exc_info
