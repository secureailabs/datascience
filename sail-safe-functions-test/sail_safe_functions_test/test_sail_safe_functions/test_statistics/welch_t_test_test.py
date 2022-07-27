from typing import Tuple

import pytest
from sail_safe_functions_orchestrator.statistics.welch_t_test import WelchTTest
from sail_safe_functions_test.helper_sail_safe_functions.series_federated_local import SeriesFederatedLocal
from scipy import stats


@pytest.mark.active
def test_welch_t_test_small(two_sample_small: Tuple[SeriesFederatedLocal, SeriesFederatedLocal]):
    """Preform a unpaired t-test asuming unequal varriance (welch t-test) using a smaller dataset

    Args:
        two_sample_big (Tuple[SeriesFederatedLocal, SeriesFederatedLocal]): A tuple of two federated series
    """
    # Arrange
    sample_0 = two_sample_small[0]
    sample_1 = two_sample_small[1]
    alternative = "less"

    # Act
    estimator = WelchTTest(alternative=alternative)
    t_statistic_sail, p_value_sail = estimator.run(sample_0, sample_1)
    t_statistic_scipy, p_value_scipy = estimator.run_reference(sample_0, sample_1)

    # Assert
    assert t_statistic_sail == pytest.approx(t_statistic_scipy, 0.0001)
    assert p_value_sail == pytest.approx(p_value_scipy, 0.0001)


@pytest.mark.active
def test_welch_t_test_big(two_sample_big: Tuple[SeriesFederatedLocal, SeriesFederatedLocal]):
    """Preform a unpaired t-test asuming unequal varriance (welch t-test) using a smaller dataset

    Args:
        two_sample_big (Tuple[SeriesFederatedLocal, SeriesFederatedLocal]): A tuple of two federated series
    """
    # Arrange
    sample_0 = two_sample_big[0]
    sample_1 = two_sample_big[1]
    alternative = "less"

    # Act
    estimator = WelchTTest(alternative=alternative)
    t_statistic_sail, p_value_sail = estimator.run(sample_0, sample_1)
    t_statistic_scipy, p_value_scipy = estimator.run_reference(sample_0, sample_1)

    # Assert
    assert t_statistic_sail == pytest.approx(t_statistic_scipy, 0.0001)
    assert p_value_sail == pytest.approx(p_value_scipy, 0.0001)
