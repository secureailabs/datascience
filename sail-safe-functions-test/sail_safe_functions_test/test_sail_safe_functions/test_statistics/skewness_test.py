import numpy as np
import pytest
from sail_safe_functions_orchestrator.statistics.skewness_federate import SkewnessFederate
from sail_safe_functions_test.helper_sail_safe_functions.series_federated_local import SeriesFederatedLocal
from scipy import stats


@pytest.mark.active
def test_skewness(one_sample_big: SeriesFederatedLocal):
    """This test our federated Skewness module

    :param one_sample_big: A single federated series fixture
    :type one_sample_big: SeriesFederatedLocal
    """

    # Arrange
    sample_0 = one_sample_big

    # Act
    # Calling fedrated sail skewness method
    skewness_sail = SkewnessFederate.skewness(sample_0)
    skewness_scipy = stats.skew(sample_0.to_numpy())

    # Assert
    assert skewness_scipy == pytest.approx(skewness_sail, 0.0001)
