import pytest
from sail_orchestrator_lib.statistics import spearman, spearman_local


@pytest.mark.active
def test_spearman_two_sided(
    connect_to_three_VMs,
    two_sample_big_remote,
    two_sample_big_local,
):
    """
    This is our test for the Sails federated Spearman

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
    spearman_sail, p_value_sail = spearman(clients, sample_0_remote, sample_1_remote, alternative)
    spearman_scipy, p_value_scipy = spearman_local(sample_0_local, sample_1_local)

    # Assert
    assert spearman_scipy == pytest.approx(spearman_sail, 0.0001)
    assert p_value_scipy == pytest.approx(p_value_sail, 0.0001)


@pytest.mark.active
def test_spearman_less(
    connect_to_three_VMs,
    two_sample_big_remote,
    two_sample_big_local,
):
    """
    This is our test for the Sails federated Spearman

    :param two_sample_big:
    :type two_sample_big: Tuple[SeriesFederatedLocal, SeriesFederatedLocal]
    """
    # Arrange
    sample_0_remote = two_sample_big_remote[0]
    sample_1_remote = two_sample_big_remote[1]
    sample_0_local = two_sample_big_local[0]
    sample_1_local = two_sample_big_local[1]
    alternative = "less"
    clients = connect_to_three_VMs

    # Act
    spearman_sail, p_value_sail = spearman(clients, sample_0_remote, sample_1_remote, alternative)
    spearman_scipy, p_value_scipy = spearman_local(sample_0_local, sample_1_local, alternative)

    # Assert
    assert spearman_scipy == pytest.approx(spearman_sail, 0.0001)
    assert p_value_scipy == pytest.approx(p_value_sail, 0.0001)


@pytest.mark.active
def test_spearman_greater(
    connect_to_three_VMs,
    two_sample_big_remote,
    two_sample_big_local,
):
    """
    This is our test for the Sails federated Spearman

    :param two_sample_big:
    :type two_sample_big: Tuple[SeriesFederatedLocal, SeriesFederatedLocal]
    """
    # Arrange
    sample_0_remote = two_sample_big_remote[0]
    sample_1_remote = two_sample_big_remote[1]
    sample_0_local = two_sample_big_local[0]
    sample_1_local = two_sample_big_local[1]
    alternative = "greater"
    clients = connect_to_three_VMs

    # Act
    spearman_sail, p_value_sail = spearman(clients, sample_0_remote, sample_1_remote, alternative)
    spearman_scipy, p_value_scipy = spearman_local(sample_0_local, sample_1_local, alternative)

    # Assert
    assert spearman_scipy == pytest.approx(spearman_sail, 0.0001)
    assert p_value_scipy == pytest.approx(p_value_sail, 0.0001)
