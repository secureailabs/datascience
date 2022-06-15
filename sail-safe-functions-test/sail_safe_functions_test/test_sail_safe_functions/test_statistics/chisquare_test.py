from typing import Tuple

import pytest
from sail_safe_functions_orchestrator.statistics.chisquare_federate import ChisquareFederate
from sail_safe_functions_test.helper_sail_safe_functions.series_federated_local import SeriesFederatedLocal
from scipy import stats


@pytest.mark.active
def test_chisquare(two_sample_categorical: Tuple[SeriesFederatedLocal, SeriesFederatedLocal]):
    """
    This is our test for the Sails federated chisquare test

    :param two_sample_categorical a dataset with cathegorical data
    :type two_sample_categorical: Tuple[SeriesFederatedLocal, SeriesFederatedLocal]
    """
    # Arrange
    sample_0 = two_sample_categorical[0]
    sample_1 = two_sample_categorical[1]

    # Act
    pearson_sail, p_value_sail = ChisquareFederate.run(sample_0, sample_1)
    pearson_scipy, p_value_scipy = ChisquareFederate.run_reference(sample_0, sample_1)

    # Assert
    assert pearson_scipy == pytest.approx(pearson_sail, 0.0001)
    assert p_value_scipy == pytest.approx(p_value_sail, 0.0001)
