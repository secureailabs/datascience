from typing import Tuple

import pytest
from sail_safe_functions_orchestrator.statistics.levene_test import LeveneTest
from sail_safe_functions_test.helper_sail_safe_functions.series_federated_local import (
    SeriesFederatedLocal,
)
from scipy.stats import levene
from sklearn.cluster import estimate_bandwidth


@pytest.mark.active
def test_levene(
    two_sample_small_two: Tuple[SeriesFederatedLocal, SeriesFederatedLocal]
):
    """
    This is our test for the Sails federated Levene test

    :param two_sample_small_two:
    :type two_sample_small_two: Tuple[SeriesFederatedLocal, SeriesFederatedLocal]
    """
    # Arrange
    sample_0 = two_sample_small_two[0]
    sample_1 = two_sample_small_two[1]

    # Act
    estimator = LeveneTest()
    f_statistic_sail, p_value_sail = estimator.run(sample_0, sample_1)
    f_statistic_scipy, p_value_scipy = estimator.run_reference(sample_0, sample_1)

    # Assert
    assert f_statistic_scipy == pytest.approx(f_statistic_sail, 0.0001)
    assert p_value_scipy == pytest.approx(p_value_sail, 0.0001)
