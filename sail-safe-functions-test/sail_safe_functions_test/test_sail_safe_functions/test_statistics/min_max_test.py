import pytest
from sail_safe_functions_orchestrator.statistics.min_max import MinMax
from sail_safe_functions_test.helper_sail_safe_functions.series_federated_local import (
    SeriesFederatedLocal,
)
import numpy


@pytest.mark.active
def test_min_max(one_sample_big: SeriesFederatedLocal):
    """This test our federated Skewness module

    :param one_sample_big: A single federated series fixture
    :type one_sample_big: SeriesFederatedLocal
    """

    # Arrange
    sample_0 = one_sample_big

    # Act
    estimator = MinMax()
    min_sail, max_sail = estimator.run(sample_0)
    min_numpy, max_numpy = estimator.run_reference(sample_0)

    # Assert
    assert max_numpy <= max_sail
    assert min_numpy >= min_sail


@pytest.mark.active
def test_min_max_empty():
    """
    This is our test to raise exception for empty
    """
    # Arrange
    numpy.random.seed(42)
    sample_size = 0
    sample_0 = SeriesFederatedLocal.from_array("dataset_0", "series_0", numpy.random.normal(0, 1, sample_size))
    # Act
    estimator = MinMax()

    with pytest.raises(Exception) as exc_info:
        #   pearson_sail, p_value_sail = estimator.run(sample_0, sample_1)
        estimator.run(sample_0)

    # Assert
    assert "series cannot be empty" in str(exc_info.value)


@pytest.mark.active
def test_min_max_one_value():
    """
    This is our test to raise exception for series containing only one value
    """
    # Arrange
    numpy.random.seed(42)
    sample_size = 1
    sample_0 = SeriesFederatedLocal.from_array("dataset_0", "series_0", numpy.random.normal(0, 1, sample_size))
    # Act
    estimator = MinMax()

    with pytest.raises(Exception) as exc_info:
        #   pearson_sail, p_value_sail = estimator.run(sample_0, sample_1)
        estimator.run(sample_0)

    # Assert
    assert "series cannot containt only one value" in str(exc_info.value)
