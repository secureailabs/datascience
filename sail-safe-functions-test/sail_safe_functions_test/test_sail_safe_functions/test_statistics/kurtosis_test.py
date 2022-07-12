import pytest
from sail_safe_functions_orchestrator.statistics.kurtosis import Kurtosis
from sail_safe_functions_test.helper_sail_safe_functions.series_federated_local import SeriesFederatedLocal
from scipy import stats


@pytest.mark.active
def test_kurtosis(one_sample_big: SeriesFederatedLocal):
    """
    This test our federated kurtosis module

    Args:
        one_sample_big (SeriesFederatedLocal): A single federated series fixture
    """
    # Arrange
    sample_0 = one_sample_big

    # Act
    estimator = Kurtosis()
    kurtosis_sail = estimator.run(sample_0)
    kurtosis_scipy = estimator.run_reference(sample_0)

    # Assert
    assert kurtosis_scipy == pytest.approx(kurtosis_sail, 0.0001)
