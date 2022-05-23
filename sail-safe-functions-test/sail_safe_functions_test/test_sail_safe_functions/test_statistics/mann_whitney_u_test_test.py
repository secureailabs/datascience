import numpy
import pandas
import pytest
from sail_safe_functions_orchestrator.statistics.mann_whitney_u_test_federate import MannWhitneyUTestFederate
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
    sample_0 = SeriesFederatedLocal()
    sample_0.add_series("dataset_0", pandas.Series(numpy.random.normal(0, 1, sample_size)))
    sample_1 = SeriesFederatedLocal()
    sample_1.add_series("dataset_0", pandas.Series(numpy.random.normal(0, 1, sample_size)))
    alternative = "two-sided"
    # Act
    w_statistic_sail, p_value_sail = MannWhitneyUTestFederate.run(
        sample_0, sample_1, alternative=alternative, type_ranking="unsafe"
    )
    w_statistic_scipy, p_value_scipy = MannWhitneyUTestFederate.run_reference(
        sample_0, sample_1, alternative=alternative
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
    sample_0 = SeriesFederatedLocal()
    sample_0.add_series("dataset_0", pandas.Series(numpy.random.normal(0, 1, sample_size)))
    sample_1 = SeriesFederatedLocal()
    sample_1.add_series("dataset_0", pandas.Series(numpy.random.normal(0, 1, sample_size)))
    alternative = "less"
    # Act
    w_statistic_sail, p_value_sail = MannWhitneyUTestFederate.run(
        sample_0, sample_1, alternative=alternative, type_ranking="unsafe"
    )
    w_statistic_scipy, p_value_scipy = MannWhitneyUTestFederate.run_reference(
        sample_0, sample_1, alternative=alternative
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
    sample_0 = SeriesFederatedLocal()
    sample_0.add_series("dataset_0", pandas.Series(numpy.random.normal(0, 1, sample_size)))
    sample_1 = SeriesFederatedLocal()
    sample_1.add_series("dataset_0", pandas.Series(numpy.random.normal(0, 1, sample_size)))
    alternative = "greater"
    # Act
    w_statistic_sail, p_value_sail = MannWhitneyUTestFederate.run(
        sample_0, sample_1, alternative=alternative, type_ranking="unsafe"
    )
    w_statistic_scipy, p_value_scipy = MannWhitneyUTestFederate.run_reference(
        sample_0, sample_1, alternative=alternative
    )

    # Assert
    assert w_statistic_scipy == pytest.approx(w_statistic_sail, 0.0001)
    assert p_value_scipy == pytest.approx(p_value_sail, 0.0001)