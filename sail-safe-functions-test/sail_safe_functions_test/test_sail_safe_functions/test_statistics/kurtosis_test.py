import pytest
from sail_safe_functions_orchestrator.statistics.kurtosis_federate import KurtosisFederate
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
    kurtosis_sail = KurtosisFederate.kurtosis(sample_0)
    kurtosis_scipy = stats.kurtosis(sample_0.to_numpy())

    # Assert
    assert kurtosis_scipy == pytest.approx(kurtosis_sail, 0.0001)
