from typing import Tuple

import pytest
from sail_safe_functions_orchestrator import statistics
from sail_safe_functions_orchestrator.series_federated import SeriesFederated
from sail_safe_functions_orchestrator.statistics.chisquare import Chisquare
from sail_safe_functions_test.helper_sail_safe_functions.series_federated_local import SeriesFederatedLocal
import numpy


@pytest.mark.active
def test_chisquare_direct(two_sample_categorical: Tuple[SeriesFederated, SeriesFederated]):
    """
    This is our test for the Sails federated chisquare test

    :param two_sample_categorical a dataset with cathegorical data
    :type two_sample_categorical: Tuple[SeriesFederated, SeriesFederated]
    """
    # Arrange
    sample_0 = two_sample_categorical[0]
    sample_1 = two_sample_categorical[1]

    # Act
    statistics.chisquare(sample_0, sample_1)


@pytest.mark.active
def test_chisquare(two_sample_categorical: Tuple[SeriesFederated, SeriesFederated]):
    """
    This is our test for the Sails federated chisquare test

    :param two_sample_categorical a dataset with cathegorical data
    :type two_sample_categorical: Tuple[SeriesFederatedLocal, SeriesFederatedLocal]
    """
    # Arrange
    sample_0 = two_sample_categorical[0]
    sample_1 = two_sample_categorical[1]

    # Act
    estimator = Chisquare()
    pearson_sail, p_value_sail = estimator.run(sample_0, sample_1)
    pearson_scipy, p_value_scipy = estimator.run_reference(sample_0, sample_1)

    # Assert
    assert pearson_scipy == pytest.approx(pearson_sail, 0.0001)
    assert p_value_scipy == pytest.approx(p_value_sail, 0.0001)


@pytest.mark.active
def test_chisquare_empty():
    """
    This is our test to raise exception for empty
    """
    # Arrange
    numpy.random.seed(42)
    sample_size = 0
    sample_0 = SeriesFederatedLocal.from_array("dataset_0", "series_0", numpy.random.normal(0, 1, sample_size))
    sample_1 = SeriesFederatedLocal.from_array("dataset_0", "series_0", numpy.random.normal(0, 1, sample_size))
    estimator = Chisquare()

    with pytest.raises(Exception) as exc_info:
        estimator.run(sample_0, sample_1)

    # Assert
    assert "series cannot be empty" in str(exc_info.value)


@pytest.mark.active
def test_chisquare_one_value():
    """
    This is our test to raise exception for only one value
    """
    # Arrange
    numpy.random.seed(42)
    sample_size = 1
    sample_0 = SeriesFederatedLocal.from_array("dataset_0", "series_0", numpy.random.normal(0, 1, sample_size))
    sample_1 = SeriesFederatedLocal.from_array("dataset_0", "series_0", numpy.random.normal(0, 1, sample_size))
    estimator = Chisquare()

    with pytest.raises(Exception) as exc_info:
        estimator.run(sample_0, sample_1)

    # Assert
    assert "series cannot containt only one value" in str(exc_info.value)


@pytest.mark.active
def test_chisquare_nan_value():
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
    estimator = Chisquare()

    with pytest.raises(Exception) as exc_info:
        estimator.run(sample_0, sample_1)

    # Assert
    assert "series cannot containt nan or None values" in str(exc_info.value)
