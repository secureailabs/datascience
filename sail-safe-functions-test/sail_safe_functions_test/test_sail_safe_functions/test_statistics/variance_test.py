import pytest
from sail_safe_functions_orchestrator.statistics import variance, variance_local


@pytest.mark.active
def test_variance(
    connect_to_three_VMs,
    one_sample_big_remote,
    one_sample_big_local,
):
    """A test of the variance statistic

    Args:
        one_sample_big (SeriesFederatedLocal): A single federated series fixture
    """
    # Arrange
    sample_0_remote = one_sample_big_remote
    sample_0_local = one_sample_big_local
    clients = connect_to_three_VMs

    #
    variance_sail = variance(clients, sample_0_remote)
    variance_numpy = variance_local(sample_0_local)

    # Assert
    assert variance_sail == pytest.approx(variance_numpy, 0.0001)
