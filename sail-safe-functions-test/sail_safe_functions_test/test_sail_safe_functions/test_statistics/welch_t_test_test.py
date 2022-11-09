from typing import Tuple

import pytest
from sail_safe_functions_orchestrator.statistics.welch_t_test import WelchTTest
from sail_safe_functions_test.helper_sail_safe_functions.series_federated_local import (
    SeriesFederatedLocal,
)
from scipy import stats
import numpy


@pytest.mark.active
def test_welch_t_test_small(two_sample_small: Tuple[SeriesFederatedLocal, SeriesFederatedLocal]):
    """Preform a unpaired t-test asuming unequal variance (welch t-test) using a smaller dataset

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
    """Preform a unpaired t-test asuming unequal variance (welch t-test) using a smaller dataset

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


@pytest.mark.active
def test_welch_t_test_empty():
    """
    This is our test to raise exception for empty
    """
    # Arrange
    numpy.random.seed(42)
    sample_size = 0
    sample_0 = SeriesFederatedLocal.from_array("dataset_0", "series_0", numpy.random.normal(0, 1, sample_size))
    sample_1 = SeriesFederatedLocal.from_array("dataset_0", "series_0", numpy.random.normal(0, 1, sample_size))
    alternative = "less"
    estimator = WelchTTest(alternative=alternative)

    with pytest.raises(Exception) as exc_info:
        #   pearson_sail, p_value_sail = estimator.run(sample_0, sample_1)
        estimator.run(sample_0, sample_1)

    # Assert
    assert "series cannot be empty" in str(exc_info.value)


@pytest.mark.active
def test_welch_t_test_one_value():
    """
    This is our test to raise exception for series containing only one value
    """
    # Arrange
    numpy.random.seed(42)
    sample_size = 1
    sample_0 = SeriesFederatedLocal.from_array("dataset_0", "series_0", numpy.random.normal(0, 1, sample_size))
    sample_1 = SeriesFederatedLocal.from_array("dataset_0", "series_0", numpy.random.normal(0, 1, sample_size))
    alternative = "less"
    estimator = WelchTTest(alternative=alternative)

    with pytest.raises(Exception) as exc_info:
        #   pearson_sail, p_value_sail = estimator.run(sample_0, sample_1)
        estimator.run(sample_0, sample_1)

    # Assert
    assert "series cannot containt only one value" in str(exc_info.value)
