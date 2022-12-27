import numpy
import pytest
from sail_safe_functions.aggregator.series_federated import SeriesFederated
from sail_safe_functions.aggregator.statistics.skewness import Skewness
from sail_safe_functions.test.helper_sail_safe_functions.tools_data_test import ToolsDataTest


@pytest.mark.active
def test_skewness(one_sample_big: SeriesFederated):
    """This test our federated Skewness module against the reference implementation"""

    # Arrange
    sample_0 = one_sample_big

    # Act
    estimator = Skewness()
    skewness_sail = estimator.run(sample_0)
    skewness_scipy = estimator.run_reference(sample_0)

    # Assert
    assert skewness_scipy == pytest.approx(skewness_sail, 0.0001)


@pytest.mark.active
def test_skewness_empty():
    """
    This is our test to raise exception for empty
    """
    # Arrange
    numpy.random.seed(42)
    sample_size = 0
    sample_0 = ToolsDataTest.from_array("dataset_0", "series_0", numpy.random.normal(0, 1, sample_size))
    # Act
    estimator = Skewness()

    with pytest.raises(Exception) as exc_info:
        estimator.run(sample_0)

    # Assert
    assert "series cannot be empty" in str(exc_info.value)


@pytest.mark.active
def test_skewness_one_value():
    """
    This is our test to raise exception for series containing only one value
    """
    # Arrange
    numpy.random.seed(42)
    sample_size = 1
    sample_0 = ToolsDataTest.from_array("dataset_0", "series_0", numpy.random.normal(0, 1, sample_size))
    # Act
    estimator = Skewness()

    with pytest.raises(Exception) as exc_info:
        estimator.run(sample_0)

    # Assert
    assert "series cannot containt only one value" in str(exc_info.value)


@pytest.mark.active
def test_skewness_nan_value():
    """
    This is our test to raise exception for series containing nan value
    """
    # Arrange
    numpy.random.seed(42)

    a = numpy.empty((20))
    a[12:] = numpy.nan
    sample_0 = ToolsDataTest.from_array("dataset_0", "series_0", a)
    # Act
    estimator = Skewness()

    with pytest.raises(Exception) as exc_info:
        estimator.run(sample_0)

    # Assert
    assert "series cannot containt nan or None values" in str(exc_info.value)
