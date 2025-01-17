from typing import Tuple

import numpy
import pytest
from sail_safe_functions.aggregator.series_federated import SeriesFederated
from sail_safe_functions.aggregator.statistics.pearson import Pearson
from sail_safe_functions.test.helper_sail_safe_functions.estimator_two_sample_reference import (
    EstimatorTwoSampleReference,
)
from sail_safe_functions.test.helper_sail_safe_functions.tools_data_test import ToolsDataTest


@pytest.mark.active
def test_pearson(two_sample_big: Tuple[SeriesFederated, SeriesFederated]):
    """
    This is our test for the Sails federated Pearson

    :param two_sample_big:
    :type two_sample_big: Tuple[SeriesFederated, SeriesFederated]
    """
    # Arrange
    sample_0 = two_sample_big[0]
    sample_1 = two_sample_big[1]
    alternative = "two-sided"

    # Act
    estimator = Pearson(alternative=alternative)
    pearson_sail, p_value_sail = estimator.run(sample_0, sample_1)
    estimator_reference = EstimatorTwoSampleReference(estimator)
    pearson_scipy, p_value_scipy = estimator_reference.run(sample_0, sample_1)

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
    sample_0 = ToolsDataTest.from_array("dataset_0", "series_0", numpy.random.normal(0, 1, sample_size))
    sample_1 = ToolsDataTest.from_array("dataset_0", "series_0", numpy.random.normal(0, 1, sample_size))
    alternative = "two-sided"

    # Act
    estimator = Pearson(alternative=alternative)
    with pytest.raises(Exception) as exc_info:
        estimator.run(sample_0, sample_1)

    # Assert
    assert "series cannot be empty" in str(exc_info.value)


@pytest.mark.active
def test_pearson_one_value():
    """
    This is our test to raise exception for series containing one value
    """
    # Arrange
    numpy.random.seed(42)
    sample_size = 1
    sample_0 = ToolsDataTest.from_array("dataset_0", "series_0", numpy.random.normal(0, 1, sample_size))
    sample_1 = ToolsDataTest.from_array("dataset_0", "series_0", numpy.random.normal(0, 1, sample_size))
    alternative = "two-sided"

    # Act
    estimator = Pearson(alternative=alternative)
    with pytest.raises(Exception) as exc_info:
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
    sample_0 = ToolsDataTest.from_array("dataset_0", "series_0", a)
    sample_1 = ToolsDataTest.from_array("dataset_0", "series_0", numpy.random.normal(0, 1, sample_size))
    alternative = "two-sided"

    # Act
    estimator = Pearson(alternative=alternative)
    with pytest.raises(Exception) as exc_info:
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
    sample_0 = ToolsDataTest.from_array("dataset_0", "series_0", numpy.random.normal(0, 1, sample_size))
    estimator = Pearson(alternative=alternative)
    pearson_sail, p_value_sail = estimator.run(sample_0, sample_0)
    estimator_reference = EstimatorTwoSampleReference(estimator)
    pearson_scipy, p_value_scipy = estimator_reference.run(sample_0, sample_0)
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

    sample_0 = ToolsDataTest.from_array("dataset_0", "series_0", numpy.array([1, 2, 3, 4, 5]))
    sample_1 = ToolsDataTest.from_array("dataset_0", "series_1", numpy.array([-1, -2, -3, -4, -5]))

    alternative = "two-sided"
    estimator = Pearson(alternative=alternative)
    pearson_sail, p_value_sail = estimator.run(sample_0, sample_1)
    estimator_reference = EstimatorTwoSampleReference(estimator)
    pearson_scipy, p_value_scipy = estimator_reference.run(sample_0, sample_1)

    # Assert
    assert pearson_scipy == pytest.approx(pearson_sail, 0.0001)
    assert p_value_scipy == pytest.approx(p_value_sail, 0.0001)


@pytest.mark.active
def test_pearson_zero_variance():
    """
    This is our test to raise exception for zero variance
    """
    # Arrange
    numpy.random.seed(42)
    sample_size = 20
    sample_0 = ToolsDataTest.from_array("dataset_0", "series_0", numpy.random.normal(0, 0, sample_size))
    sample_1 = ToolsDataTest.from_array("dataset_0", "series_0", numpy.random.normal(0, 0, sample_size))
    alternative = "two-sided"

    # Act
    estimator = Pearson(alternative=alternative)
    with pytest.raises(Exception) as exc_info:
        estimator.run(sample_0, sample_1)

    # Assert
    assert "Variance is zero raises sys.float_info.max " in str(exc_info.value)
