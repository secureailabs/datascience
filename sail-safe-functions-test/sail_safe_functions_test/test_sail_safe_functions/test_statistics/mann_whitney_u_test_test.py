import numpy
import pandas
import pytest
from sail_safe_functions_orchestrator.statistics.mann_whitney_u_test import MannWhitneyUTest
from sail_safe_functions_test.helper_sail_safe_functions.series_federated_local import SeriesFederatedLocal
from scipy import stats


@pytest.mark.active
def test_mann_whitney_u_test_two_sided():
    """
    This is our test for the two-sided mann whitney u test
    """
    # Arrange
    numpy.random.seed(42)
    sample_size = 200
    sample_0 = SeriesFederatedLocal.from_array("dataset_0", "series_0", numpy.random.normal(0, 1, sample_size))
    sample_1 = SeriesFederatedLocal.from_array("dataset_0", "series_1", numpy.random.normal(0, 1, sample_size))
    alternative = "two-sided"
    type_ranking = "unsafe"
    # Act
    estimator = MannWhitneyUTest(alternative=alternative, type_ranking=type_ranking)
    w_statistic_sail, p_value_sail = estimator.run(sample_0, sample_1)
    w_statistic_scipy, p_value_scipy = estimator.run_reference(
        sample_0,
        sample_1,
    )

    # Assert
    assert w_statistic_scipy == pytest.approx(w_statistic_sail, 0.0001)
    assert p_value_scipy == pytest.approx(p_value_sail, 0.0001)


@pytest.mark.active
def test_mann_whitney_u_test_less():
    """
    This is our test for the less mann whitney u test
    """
    # Arrange
    numpy.random.seed(42)
    sample_size = 200
    sample_0 = SeriesFederatedLocal.from_array("dataset_0", "series_0", numpy.random.normal(0, 1, sample_size))
    sample_1 = SeriesFederatedLocal.from_array("dataset_0", "series_1", numpy.random.normal(0, 1, sample_size))
    alternative = "less"
    type_ranking = "unsafe"
    # Act
    estimator = MannWhitneyUTest(alternative=alternative, type_ranking=type_ranking)
    w_statistic_sail, p_value_sail = estimator.run(sample_0, sample_1)
    w_statistic_scipy, p_value_scipy = estimator.run_reference(
        sample_0,
        sample_1,
    )

    # Assert
    assert w_statistic_scipy == pytest.approx(w_statistic_sail, 0.0001)
    assert p_value_scipy == pytest.approx(p_value_sail, 0.0001)


@pytest.mark.active
def test_mann_whitney_u_test_greater():
    """
    This is our test for the greater mann whitney u test
    """
    # Arrange
    numpy.random.seed(42)
    sample_size = 200
    sample_0 = SeriesFederatedLocal.from_array("dataset_0", "series_0", numpy.random.normal(0, 1, sample_size))
    sample_1 = SeriesFederatedLocal.from_array("dataset_0", "series_1", numpy.random.normal(0, 1, sample_size))
    alternative = "greater"
    type_ranking = "unsafe"
    # Act
    estimator = MannWhitneyUTest(alternative=alternative, type_ranking=type_ranking)
    w_statistic_sail, p_value_sail = estimator.run(sample_0, sample_1)
    w_statistic_scipy, p_value_scipy = estimator.run_reference(
        sample_0,
        sample_1,
    )

    # Assert
    assert w_statistic_scipy == pytest.approx(w_statistic_sail, 0.0001)
    assert p_value_scipy == pytest.approx(p_value_sail, 0.0001)


@pytest.mark.active
def testmann_whitney_u_test_empty():
    """
    This is our test to raise exception for empty
    """
    # Arrange
    numpy.random.seed(42)
    sample_size = 0
    sample_0 = SeriesFederatedLocal.from_array("dataset_0", "series_0", numpy.random.normal(0, 1, sample_size))
    sample_1 = SeriesFederatedLocal.from_array("dataset_0", "series_0", numpy.random.normal(0, 1, sample_size))
    alternative = "greater"
    type_ranking = "unsafe"
    # Act
    estimator = MannWhitneyUTest(alternative=alternative, type_ranking=type_ranking)

    with pytest.raises(Exception) as exc_info:
        #   pearson_sail, p_value_sail = estimator.run(sample_0, sample_1)
        estimator.run(sample_0, sample_1)

    # Assert
    assert "series cannot be empty" == exc_info
