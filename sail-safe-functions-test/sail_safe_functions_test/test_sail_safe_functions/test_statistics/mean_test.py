import pytest
from sail_orchestrator_lib.statistics import mean, mean_local


@pytest.mark.active
def test_mean(
    connect_to_three_VMs,
    one_sample_big_remote,
    one_sample_big_local,
):
    """A test of the mean value statisc

    Args:
        one_sample_big (SeriesFederatedLocal): A single federated series fixture
    """
    # Arrange
    sample_0_local = one_sample_big_local
    sample_0_remote = one_sample_big_remote
    clients = connect_to_three_VMs

    # Act
    mean_sail = mean(clients, sample_0_remote)
    mean_numpy = mean_local(sample_0_local)

    # Assert
    assert mean_sail == pytest.approx(mean_numpy, 0.0001)
