from typing import Tuple

import pytest
from sail_safe_functions_orchestrator.statistics.pearson_federate import PearsonFederate
from sail_safe_functions_test.helper_sail_safe_functions.series_federated_local import SeriesFederatedLocal
from scipy import stats


@pytest.mark.active
def test_pearson(two_sample_big: Tuple[SeriesFederatedLocal, SeriesFederatedLocal]):
    """
    This is our test for the Sails federated Pearson

    :param two_sample_big:
    :type two_sample_big: Tuple[SeriesFederatedLocal, SeriesFederatedLocal]
    """
    # Arrange
    sample_0 = two_sample_big[0]
    sample_1 = two_sample_big[1]

    # Act
    pearson_sail, p_value_sail = PearsonFederate.pearson(sample_0, sample_1, "two-sided")
    pearson_scipy, p_value_scipy = stats.pearsonr(sample_0.to_numpy(), sample_1.to_numpy())

    # Assert
    assert pearson_scipy == pytest.approx(pearson_sail, 0.0001)
    assert p_value_scipy == pytest.approx(p_value_sail, 0.0001)
