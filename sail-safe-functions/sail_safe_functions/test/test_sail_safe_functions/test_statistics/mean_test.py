import numpy
import numpy as np
import pytest
from sail_safe_functions.aggregator import statistics
from sail_safe_functions.aggregator.series_federated import SeriesFederated
from sail_safe_functions.aggregator.statistics.mean import Mean
from sail_safe_functions.test.helper_sail_safe_functions.tools_data_test import ToolsDataTest


@pytest.mark.active
def test_mean_direct(one_sample_big: SeriesFederated):
    statistics.mean(one_sample_big)


@pytest.mark.active
def test_mean(one_sample_big: SeriesFederated):
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
    sample_0 = ToolsDataTest.from_array("dataset_0", "series_0", numpy.random.normal(0, 1, sample_size))
    # Act
    estimator = Mean()

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
    estimator = Mean()

    with pytest.raises(Exception) as exc_info:
        estimator.run(sample_0)

    # Assert
    assert "series cannot containt only one value" in str(exc_info.value)


@pytest.mark.active
def test_mean_nan_value():
    """
    This is our test to raise exception if series containing nan values
    """
    # Arrange
    numpy.random.seed(42)
    a = numpy.empty((20))
    a[12:] = numpy.nan
    sample_0 = ToolsDataTest.from_array("dataset_0", "series_0", a)
    # Act
    estimator = Mean()

    with pytest.raises(Exception) as exc_info:
        estimator.run(sample_0)

    # Assert
    assert "series cannot containt nan or None values" in str(exc_info.value)
