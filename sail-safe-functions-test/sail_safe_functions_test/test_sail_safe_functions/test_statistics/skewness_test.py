import pytest
from sail_safe_functions_orchestrator.statistics.skewness import Skewness
from sail_safe_functions_test.helper_sail_safe_functions.series_federated_local import (
    SeriesFederatedLocal,
)
from scipy import stats
import numpy


@pytest.mark.active
def test_skewness(one_sample_big: SeriesFederatedLocal):
    """This test our federated Skewness module

    :param one_sample_big: A single federated series fixture
    :type one_sample_big: SeriesFederatedLocal
    """

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
    sample_0 = SeriesFederatedLocal.from_array("dataset_0", "series_0", numpy.random.normal(0, 1, sample_size))
    # Act
    estimator = Skewness()

    with pytest.raises(Exception) as exc_info:
        #   pearson_sail, p_value_sail = estimator.run(sample_0, sample_1)
        estimator.run(sample_0)

    # Assert
    assert "series cannot be empty" == exc_info
