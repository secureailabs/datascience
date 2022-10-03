import pytest
from sail_orchestrator_lib.statistics import skewness, skewness_local


@pytest.mark.active
def test_skewness(
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
    skewness_sail = skewness(clients, sample_0_remote)
    skewness_scipy = skewness_local(sample_0_local)

    # Assert
    assert skewness_scipy == pytest.approx(skewness_sail, 0.0001)
