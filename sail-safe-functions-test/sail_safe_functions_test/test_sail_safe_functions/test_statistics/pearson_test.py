from typing import Tuple

import pytest
from sail_safe_functions_orchestrator.statistics.pearson import Pearson
from sail_safe_functions_test.helper_sail_safe_functions.series_federated_local import (
    SeriesFederatedLocal,
)
from scipy import stats
import numpy


@pytest.mark.active
def test_pearson(two_sample_big: Tuple[SeriesFederatedLocal, SeriesFederatedLocal]):
    """
    This is our test for the Sails federated Pearson

    :param two_sample_big:
    :type two_sample_big: Tuple[SeriesFederatedLocal, SeriesFederatedLocal]
    """
    # Arrange
    sample_0 = two_sample_big[0]
    sample_1 = two_sample_big[1]
    alternative = "two-sided"

    # Act
    estimator = Pearson(alternative=alternative)
    pearson_sail, p_value_sail = estimator.run(sample_0, sample_1)
    pearson_scipy, p_value_scipy = estimator.run_reference(sample_0, sample_1)

    # Assert
    assert pearson_scipy == pytest.approx(pearson_sail, 0.0001)
    assert p_value_scipy == pytest.approx(p_value_sail, 0.0001)


@pytest.mark.active
def test_pearson_empty():
    """
    This is our test to raise exception for empty
    """
    # Arrange
    numpy.random.seed(42)
    sample_size = 0
    sample_0 = SeriesFederatedLocal.from_array("dataset_0", "series_0", numpy.random.normal(0, 1, sample_size))
    sample_1 = SeriesFederatedLocal.from_array("dataset_0", "series_0", numpy.random.normal(0, 1, sample_size))
    alternative = "two-sided"

    # Act
    estimator = Pearson(alternative=alternative)
    with pytest.raises(Exception) as exc_info:
        #   pearson_sail, p_value_sail = estimator.run(sample_0, sample_1)
        estimator.run(sample_0, sample_1)

    # Assert
    assert "series cannot be empty" in str(exc_info.value)


@pytest.mark.active
def test_pearson_one_value():
    """
    This is our test to raise exception for series containing only one value
    """
    # Arrange
    numpy.random.seed(42)
    sample_size = 1
    sample_0 = SeriesFederatedLocal.from_array("dataset_0", "series_0", numpy.random.normal(0, 1, sample_size))
    sample_1 = SeriesFederatedLocal.from_array("dataset_0", "series_0", numpy.random.normal(0, 1, sample_size))
    alternative = "two-sided"

    # Act
    estimator = Pearson(alternative=alternative)
    with pytest.raises(Exception) as exc_info:
        #   pearson_sail, p_value_sail = estimator.run(sample_0, sample_1)
        estimator.run(sample_0, sample_1)

    # Assert
    assert "series cannot containt only one value" in str(exc_info.value)


@pytest.mark.active
def test_pearson_nan_value():
    """
    This is our test to raise exception if series containing nan values
    """
    # Arrange
    numpy.random.seed(42)
    sample_size = 20
    a = numpy.empty((20))
    a[12:] = numpy.nan
    sample_0 = SeriesFederatedLocal.from_array("dataset_0", "series_0", a)
    sample_1 = SeriesFederatedLocal.from_array("dataset_0", "series_0", numpy.random.normal(0, 1, sample_size))
    alternative = "two-sided"

    # Act
    estimator = Pearson(alternative=alternative)
    with pytest.raises(Exception) as exc_info:
        #   pearson_sail, p_value_sail = estimator.run(sample_0, sample_1)
        estimator.run(sample_0, sample_1)

    # Assert
    assert "series cannot containt nan or None values" in str(exc_info.value)


@pytest.mark.active
def test_pearson_same_sample():
    """
    This is our test for the Sails federated Pearson. Test where arg0 = arg1 (should return correlation of 1)

    """
    # Arrange

    alternative = "two-sided"
    sample_size = 100
    sample_0 = SeriesFederatedLocal.from_array("dataset_0", "series_0", numpy.random.normal(0, 1, sample_size))
    estimator = Pearson(alternative=alternative)
    pearson_sail, p_value_sail = estimator.run(sample_0, sample_0)
    pearson_scipy, p_value_scipy = estimator.run_reference(sample_0, sample_0)
    print(pearson_sail)
    print(pearson_scipy)
    # Assert
    assert pearson_scipy == pytest.approx(pearson_sail, 0.0001)
    assert p_value_scipy == pytest.approx(p_value_sail, 0.0001)


@pytest.mark.active
def test_pearson_same_sample_negative():
    """
    This is our test for the Sails federated Pearson. Test where arg0 = arg1 (should return correlation of 1)
    """
    numpy.random.seed(42)

    a = [1, 2, 3, 4, 5]
    b = [-1, -2, -3, -4, -5]
    a = numpy.array(a)
    b = numpy.array(b)

    sample_0 = SeriesFederatedLocal.from_array("dataset_0", "series_0", a)
    sample_1 = SeriesFederatedLocal.from_array("dataset_0", "series_0", b)

    alternative = "two-sided"
    estimator = Pearson(alternative=alternative)
    pearson_sail, p_value_sail = estimator.run(sample_0, sample_1)
    pearson_scipy, p_value_scipy = estimator.run_reference(sample_0, sample_1)

    # Assert
    assert pearson_scipy == pytest.approx(pearson_sail, 0.0001)
    # assert p_value_scipy == pytest.approx(p_value_sail, 0.0001)
