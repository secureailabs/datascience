import numpy
import pytest
from sail_safe_functions.aggregator.series_federated import SeriesFederated
from sail_safe_functions.aggregator.statistics.variance import Variance
from sail_safe_functions.test.helper_sail_safe_functions.estimator_one_sample_reference import (
    EstimatorOneSampleReference,
)
from sail_safe_functions.test.helper_sail_safe_functions.tools_data_test import ToolsDataTest


@pytest.mark.active
def test_variance(one_sample_big: SeriesFederated):
    """A test of the variance statistic

    Args:
        one_sample_big (SeriesFederated): A single federated series fixture
    """
    # Arrange
    sample_0 = one_sample_big

    #
    estimator = Variance()
    variance_sail = estimator.run(sample_0)
    estimator_reference = EstimatorOneSampleReference(estimator)
    variance_numpy = estimator_reference.run(sample_0)

    # Assert
    assert variance_sail == pytest.approx(variance_numpy, 0.0001)


@pytest.mark.active
def test_mean_empty():
    """
    This is our test to raise exception for empty
    """
    # Arrange
    numpy.random.seed(42)
    sample_size = 0
    sample_0 = ToolsDataTest.from_array("dataset_0", "series_0", numpy.random.normal(0, 1, sample_size))
    # Act
    estimator = Variance()

    with pytest.raises(Exception) as exc_info:
        estimator.run(sample_0)

    # Assert
    assert "series cannot be empty" in str(exc_info.value)


@pytest.mark.active
def test_mean_one_value():
    """
    This is our test to raise exception for series containing only one value
    """
    # Arrange
    numpy.random.seed(42)
    sample_size = 1
    sample_0 = ToolsDataTest.from_array("dataset_0", "series_0", numpy.random.normal(0, 1, sample_size))
    # Act
    estimator = Variance()

    with pytest.raises(Exception) as exc_info:
        estimator.run(sample_0)

    # Assert
    assert "series cannot containt only one value" in str(exc_info.value)


@pytest.mark.active
def test_mean_nan_value():
    """
    This is our test to raise exception for series containing nan value
    """
    # Arrange
    a = numpy.empty((20))
    a[12:] = numpy.nan
    sample_0 = ToolsDataTest.from_array("dataset_0", "series_0", a)
    # Act
    estimator = Variance()

    with pytest.raises(Exception) as exc_info:
        estimator.run(sample_0)

    # Assert
    assert "series cannot containt nan or None values" in str(exc_info.value)
