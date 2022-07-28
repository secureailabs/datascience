import numpy as np
import pytest
from sail_safe_functions_orchestrator.statistics.variance import Variance
from sail_safe_functions_test.helper_sail_safe_functions.series_federated_local import (
    SeriesFederatedLocal,
)


@pytest.mark.active
def test_variance(one_sample_big: SeriesFederatedLocal):
    """A test of the variance statistic

    Args:
        one_sample_big (SeriesFederatedLocal): A single federated series fixture
    """
    # Arrange
    sample_0 = one_sample_big

    #
    estimator = Variance()
    variance_sail = estimator.run(sample_0)
    variance_numpy = estimator.run_reference(sample_0)

    # Assert
    assert variance_sail == pytest.approx(variance_numpy, 0.0001)
