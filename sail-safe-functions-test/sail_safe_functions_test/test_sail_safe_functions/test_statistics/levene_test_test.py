from typing import Tuple

import pytest
from sail_safe_functions_orchestrator.statistics import levene, levene_local


@pytest.mark.active
def test_levene(
    connect_to_one_VM,
    two_sample_small_two_remote,
    two_sample_small_two_local,
):
    """
    This is our test for the Sails federated Levene test

    :param two_sample_small_two:
    :type two_sample_small_two: Tuple[SeriesFederatedLocal, SeriesFederatedLocal]
    """
    # Arrange
    sample_0_remote = two_sample_small_two_remote[0]
    sample_1_remote = two_sample_small_two_remote[1]
    sample_0_local = two_sample_small_two_local[0]
    sample_1_local = two_sample_small_two_local[1]
    clients = [connect_to_one_VM]

    # Act
    f_statistic_sail, p_value_sail = levene(clients, sample_0_remote, sample_1_remote)
    f_statistic_scipy, p_value_scipy = levene_local(sample_0_local, sample_1_local)

    # Assert
    assert f_statistic_scipy == pytest.approx(f_statistic_sail, 0.0001)
    assert p_value_scipy == pytest.approx(p_value_sail, 0.0001)
