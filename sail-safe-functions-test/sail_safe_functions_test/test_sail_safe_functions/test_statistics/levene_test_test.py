from typing import Tuple

import pytest
from sail_safe_functions_orchestrator.statistics.levene_test import LeveneTest
from sail_safe_functions_test.helper_sail_safe_functions.series_federated_local import (
    SeriesFederatedLocal,
)
from scipy.stats import levene
from sklearn.cluster import estimate_bandwidth
import numpy


@pytest.mark.active
def test_levene(two_sample_small_two: Tuple[SeriesFederatedLocal, SeriesFederatedLocal]):
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


@pytest.mark.active
def test_levens_empty():
    """
    This is our test to raise exception for empty
    """
    # Arrange
    numpy.random.seed(42)
    sample_size = 0
    sample_0 = SeriesFederatedLocal.from_array("dataset_0", "series_0", numpy.random.normal(0, 1, sample_size))
    sample_1 = SeriesFederatedLocal.from_array("dataset_0", "series_0", numpy.random.normal(0, 1, sample_size))
    estimator = LeveneTest()

    # Act
    with pytest.raises(Exception) as exc_info:
        estimator.run(sample_0, sample_1)

    # Assert
    assert "series cannot be empty" in str(exc_info.value)


@pytest.mark.active
def test_levens_one_value():
    """
    This is our test to raise exception for series containing only one value

    """
    # Arrange
    numpy.random.seed(42)
    sample_size = 1
    sample_0 = SeriesFederatedLocal.from_array("dataset_0", "series_0", numpy.random.normal(0, 1, sample_size))
    sample_1 = SeriesFederatedLocal.from_array("dataset_0", "series_0", numpy.random.normal(0, 1, sample_size))
    estimator = LeveneTest()

    # Act
    with pytest.raises(Exception) as exc_info:
        estimator.run(sample_0, sample_1)

    # Assert
    assert "series cannot containt only one value" in str(exc_info.value)


@pytest.mark.active
def test_levens_nan_value():
    """
    This is our test to raise exception if series containing nan values

    """
    # Arrange
    numpy.random.seed(42)
    a = numpy.empty((20))
    a[12:] = numpy.nan
    sample_size = 20
    sample_0 = SeriesFederatedLocal.from_array("dataset_0", "series_0", a)
    sample_1 = SeriesFederatedLocal.from_array("dataset_0", "series_0", numpy.random.normal(0, 1, sample_size))
    estimator = LeveneTest()

    # Act
    with pytest.raises(Exception) as exc_info:
        estimator.run(sample_0, sample_1)

    # Assert
    assert "series cannot containt nan or None values" in str(exc_info.value)
