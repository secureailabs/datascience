import pytest
from sail_safe_functions_orchestrator.statistics import kurtosis, kurtosis_local


@pytest.mark.active
def test_kurtosis(
    connect_to_three_VMs,
    one_sample_big_remote,
    one_sample_big_local,
):
    """
    This function is here to test the sail-statistics federated kurtosis

        :param one_sample_big: Input sample values
        :type one_sample_big: SeriesFederatedLocal
    """
    # Arrange
    sample_0_local = one_sample_big_local
    sample_0_remote = one_sample_big_remote
    clients = connect_to_three_VMs

    # Act
    kurtosis_sail = kurtosis(clients, sample_0_remote)
    kurtosis_scipy = kurtosis_local(sample_0_local)

    # Assert
    assert kurtosis_scipy == pytest.approx(kurtosis_sail, 0.0001)
