import pytest
from sail_orchestrator_lib.statistics import student_t, student_t_local


@pytest.mark.active
def test_student_t_test_big(
    connect_to_three_VMs,
    two_sample_big_remote,
    two_sample_big_local,
):
    """Preform a unpaired t-test asuming equal variance

    Args:
        two_sample_big (Tuple[SeriesFederatedLocal, SeriesFederatedLocal]): A tuple of two federated series
    """
    # Arrange
    sample_0_remote = two_sample_big_remote[0]
    sample_1_remote = two_sample_big_remote[1]
    sample_0_local = two_sample_big_local[0]
    sample_1_local = two_sample_big_local[1]
    alternative = "less"
    clients = connect_to_three_VMs

    # Act
    t_statistic_sail, p_value_sail = student_t(clients, sample_0_remote, sample_1_remote)
    t_statistic_scipy, p_value_scipy = student_t_local(sample_0_local, sample_1_local, alternative)

    # Assert
    assert t_statistic_sail == pytest.approx(t_statistic_scipy, 0.0001)
    assert p_value_sail == pytest.approx(p_value_scipy, 0.0001)
