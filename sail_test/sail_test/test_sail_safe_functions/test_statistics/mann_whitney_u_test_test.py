import pytest
from sail_orchestrator_lib.statistics import mann_whitney, mann_whitney_local


@pytest.mark.active
def test_mann_whitney_u_test_two_sided(
    connect_to_one_VM,
    two_sample_normal_remote,
    two_sample_normal_local,
):
    """
    This is our test for the two-sided mann whitney u test
    """
    # Arrange
    sample_0_remote = two_sample_normal_remote[0]
    sample_1_remote = two_sample_normal_remote[1]
    sample_0_local = two_sample_normal_local[0]
    sample_1_local = two_sample_normal_local[1]
    alternative = "two-sided"
    clients = [connect_to_one_VM]

    # Act
    w_statistic_sail, p_value_sail = mann_whitney(clients, sample_0_remote, sample_1_remote, alternative)
    w_statistic_scipy, p_value_scipy = mann_whitney_local(sample_0_local, sample_1_local)

    # Assert
    assert w_statistic_scipy == pytest.approx(w_statistic_sail, 0.0001)
    assert p_value_scipy == pytest.approx(p_value_sail, 0.0001)


@pytest.mark.active
def test_mann_whitney_u_test_less(
    connect_to_one_VM,
    two_sample_normal_remote,
    two_sample_normal_local,
):
    """
    This is our test for the less mann whitney u test
    """
    # Arrange
    sample_0_remote = two_sample_normal_remote[0]
    sample_1_remote = two_sample_normal_remote[1]
    sample_0_local = two_sample_normal_local[0]
    sample_1_local = two_sample_normal_local[1]
    alternative = "less"
    clients = [connect_to_one_VM]
    # Act
    w_statistic_sail, p_value_sail = mann_whitney(clients, sample_0_remote, sample_1_remote, alternative)
    w_statistic_scipy, p_value_scipy = mann_whitney_local(sample_0_local, sample_1_local, alternative)

    # Assert
    assert w_statistic_scipy == pytest.approx(w_statistic_sail, 0.0001)
    assert p_value_scipy == pytest.approx(p_value_sail, 0.0001)


@pytest.mark.active
def test_mann_whitney_u_test_greater(
    connect_to_one_VM,
    two_sample_normal_remote,
    two_sample_normal_local,
):
    """
    This is our test for the greater mann whitney u test
    """
    # Arrange
    sample_0_remote = two_sample_normal_remote[0]
    sample_1_remote = two_sample_normal_remote[1]
    sample_0_local = two_sample_normal_local[0]
    sample_1_local = two_sample_normal_local[1]
    alternative = "greater"
    clients = [connect_to_one_VM]
    # Act
    w_statistic_sail, p_value_sail = mann_whitney(clients, sample_0_remote, sample_1_remote, alternative)
    w_statistic_scipy, p_value_scipy = mann_whitney_local(sample_0_local, sample_1_local, alternative)

    # Assert
    assert w_statistic_scipy == pytest.approx(w_statistic_sail, 0.0001)
    assert p_value_scipy == pytest.approx(p_value_sail, 0.0001)
