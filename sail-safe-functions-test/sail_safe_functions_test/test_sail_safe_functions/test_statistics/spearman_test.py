from typing import Tuple

import pytest
from sail_safe_functions_orchestrator.statistics.spearman_federate import SpearmanFederate
from sail_safe_functions_test.helper_sail_safe_functions.series_federated_local import SeriesFederatedLocal
from scipy import stats


@pytest.mark.active
def test_spearman_two_sided(two_sample_big: Tuple[SeriesFederatedLocal, SeriesFederatedLocal]):
    """
    This is our test for the Sails federated Spearman

    :param two_sample_big:
    :type two_sample_big: Tuple[SeriesFederatedLocal, SeriesFederatedLocal]
    """
    # Arrange
    sample_0 = two_sample_big[0]
    sample_1 = two_sample_big[1]

    # Act
    spearman_sail, p_value_sail = SpearmanFederate.spearman(sample_0, sample_1, alternative="two-sided", mode="unsafe")
    spearman_scipy, p_value_scipy = stats.spearmanr(sample_0.to_numpy(), sample_1.to_numpy(), alternative="two-sided")

    # Assert
    assert spearman_scipy == pytest.approx(spearman_sail, 0.0001)
    assert p_value_scipy == pytest.approx(p_value_sail, 0.0001)


@pytest.mark.active
def test_spearman_less(two_sample_big: Tuple[SeriesFederatedLocal, SeriesFederatedLocal]):
    """
    This is our test for the Sails federated Spearman

    :param two_sample_big:
    :type two_sample_big: Tuple[SeriesFederatedLocal, SeriesFederatedLocal]
    """
    # Arrange
    sample_0 = two_sample_big[0]
    sample_1 = two_sample_big[1]

    # Act
    spearman_sail, p_value_sail = SpearmanFederate.spearman(sample_0, sample_1, alternative="less", mode="unsafe")
    spearman_scipy, p_value_scipy = stats.spearmanr(sample_0.to_numpy(), sample_1.to_numpy(), alternative="less")

    # Assert
    assert spearman_scipy == pytest.approx(spearman_sail, 0.0001)
    assert p_value_scipy == pytest.approx(p_value_sail, 0.0001)


@pytest.mark.active
def test_spearman_greater(two_sample_big: Tuple[SeriesFederatedLocal, SeriesFederatedLocal]):
    """
    This is our test for the Sails federated Spearman

    :param two_sample_big:
    :type two_sample_big: Tuple[SeriesFederatedLocal, SeriesFederatedLocal]
    """
    # Arrange
    sample_0 = two_sample_big[0]
    sample_1 = two_sample_big[1]

    # Act
    spearman_sail, p_value_sail = SpearmanFederate.spearman(sample_0, sample_1, alternative="greater", mode="unsafe")
    spearman_scipy, p_value_scipy = stats.spearmanr(sample_0.to_numpy(), sample_1.to_numpy(), alternative="greater")

    # Assert
    assert spearman_scipy == pytest.approx(spearman_sail, 0.0001)
    assert p_value_scipy == pytest.approx(p_value_sail, 0.0001)
