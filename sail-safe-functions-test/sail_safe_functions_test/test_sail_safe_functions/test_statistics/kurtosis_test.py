import pytest
from sail_safe_functions_orchestrator.statistics.kurtosis import Kurtosis
from sail_safe_functions_test.helper_sail_safe_functions.series_federated_local import (
    SeriesFederatedLocal,
)
from scipy import stats
import numpy


@pytest.mark.active
def test_kurtosis(one_sample_big: SeriesFederatedLocal):
    """
    This function is here to test the sail-statistics federated kurtosis

        :param one_sample_big: Input sample values
        :type one_sample_big: SeriesFederatedLocal
    """
    # Arrange
    sample_0 = one_sample_big

    # Act
    estimator = Kurtosis()
    kurtosis_sail = estimator.run(sample_0)
    kurtosis_scipy = estimator.run_reference(sample_0)

    # Assert
    assert kurtosis_scipy == pytest.approx(kurtosis_sail, 0.0001)


@pytest.mark.active
def test_kurtosis_empty():
    """
    This is our test to raise exception for empty
    """
    # Arrange
    numpy.random.seed(42)
    sample_size = 0
    sample_0 = SeriesFederatedLocal.from_array("dataset_0", "series_0", numpy.random.normal(0, 1, sample_size))
    # Act
    estimator = Kurtosis()

    with pytest.raises(Exception) as exc_info:
        estimator.run(sample_0)

    # Assert
    assert "series cannot be empty" in str(exc_info.value)


@pytest.mark.active
def test_kurtosis_one_value():
    """
    This is our test to raise exception for series containing only one value
    """
    # Arrange
    numpy.random.seed(42)
    sample_size = 1
    sample_0 = SeriesFederatedLocal.from_array("dataset_0", "series_0", numpy.random.normal(0, 1, sample_size))
    # Act
    estimator = Kurtosis()

    with pytest.raises(Exception) as exc_info:
        estimator.run(sample_0)

    # Assert
    assert "series cannot containt only one value" in str(exc_info.value)


def test_kurtosis_nan_value():
    """
    This is our test to raise exception if series containing nan values
    """
    # Arrange
    numpy.random.seed(42)
    a = numpy.empty((20))
    a[12:] = numpy.nan
    sample_0 = SeriesFederatedLocal.from_array("dataset_0", "series_0", a)
    # Act
    estimator = Kurtosis()

    with pytest.raises(Exception) as exc_info:
        estimator.run(sample_0)

    # Assert
    assert "series cannot containt nan or None values" in str(exc_info.value)
