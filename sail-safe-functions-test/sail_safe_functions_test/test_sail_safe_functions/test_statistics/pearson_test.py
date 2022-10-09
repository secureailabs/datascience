import pytest
from sail_safe_functions_orchestrator.statistics import pearson, pearson_local


@pytest.mark.active
def test_pearson(
    connect_to_three_VMs,
    two_sample_big_remote,
    two_sample_big_local,
):
    """
    This is our test for the Sails federated Pearson

    :param two_sample_big:
    :type two_sample_big: Tuple[SeriesFederatedLocal, SeriesFederatedLocal]
    """
    # Arrange
    sample_0_remote = two_sample_big_remote[0]
    sample_1_remote = two_sample_big_remote[1]
    sample_0_local = two_sample_big_local[0]
    sample_1_local = two_sample_big_local[1]
    alternative = "two-sided"
    clients = connect_to_three_VMs

    # Act
    pearson_sail, p_value_sail = pearson(clients, sample_0_remote, sample_1_remote, alternative)
    pearson_scipy, p_value_scipy = pearson_local(sample_0_local, sample_1_local)

    # Assert
    assert pearson_scipy == pytest.approx(pearson_sail, 0.0001)
    assert p_value_scipy == pytest.approx(p_value_sail, 0.0001)
