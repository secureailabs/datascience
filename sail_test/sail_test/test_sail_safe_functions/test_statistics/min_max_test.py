import pytest
from sail_orchestrator_lib.statistics import min_max, min_max_local


@pytest.mark.active
def test_min_max(
    connect_to_three_VMs,
    one_sample_big_remote,
    one_sample_big_local,
):
    """This test our federated Skewness module

    :param one_sample_big: A single federated series fixture
    :type one_sample_big: SeriesFederatedLocal
    """

    # Arrange
    sample_0_remote = one_sample_big_remote
    sample_0_local = one_sample_big_local
    clients = connect_to_three_VMs

    # Act
    min_sail, max_sail = min_max(clients, sample_0_remote)
    min_numpy, max_numpy = min_max_local(sample_0_local)

    # Assert
    assert max_numpy <= max_sail
    assert min_numpy >= min_sail
