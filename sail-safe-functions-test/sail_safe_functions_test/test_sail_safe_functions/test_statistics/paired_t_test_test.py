from typing import Tuple

import pytest
from sail_safe_functions_orchestrator.statistics.paired_t_test_federate import \
    PairedTTestFederate
from sail_safe_functions_test.helper_sail_safe_functions.series_federated_local import \
    SeriesFederatedLocal
from scipy import stats


@pytest.mark.active
def test_t_test_paired_big(two_sample_big: Tuple[SeriesFederatedLocal, SeriesFederatedLocal]):
    """Preform a paired t-test using a bigger dataset

    Args:
        two_sample_big (Tuple[SeriesFederatedLocal, SeriesFederatedLocal]): A tuple of two federated series
    """
    # Arrange
    sample_0 = two_sample_big[0]
    sample_1 = two_sample_big[1]

    # Act
    t_statistic_sail, p_value_sail = PairedTTestFederate.ttest_rel(sample_0, sample_1, alternative="less")

    t_statistic_scipy, p_value_scipy = stats.ttest_rel(sample_0.to_numpy(), sample_1.to_numpy(), alternative="less")

    # Assert
    assert t_statistic_sail == pytest.approx(t_statistic_scipy, 0.0001)
    assert p_value_sail == pytest.approx(p_value_scipy, 0.0001)


@pytest.mark.active
def test_t_test_paired_small(two_sample_small_paired: Tuple[SeriesFederatedLocal, SeriesFederatedLocal]):
    """Preform a paired t-test using a smaller dataset

    Args:
        two_sample_big (Tuple[SeriesFederatedLocal, SeriesFederatedLocal]): A tuple of two federated series
    """
    # Arrange
    sample_0 = two_sample_small_paired[0]
    sample_1 = two_sample_small_paired[1]

    # Act
    t_statistic_sail, p_value_sail = PairedTTestFederate.ttest_rel(sample_0, sample_1, alternative="less")

    t_statistic_scipy, p_value_scipy = stats.ttest_rel(sample_0.to_numpy(), sample_1.to_numpy(), alternative="less")
    # Assert
    assert t_statistic_sail == pytest.approx(t_statistic_scipy, 0.0001)
    assert p_value_sail == pytest.approx(p_value_scipy, 0.0001)
