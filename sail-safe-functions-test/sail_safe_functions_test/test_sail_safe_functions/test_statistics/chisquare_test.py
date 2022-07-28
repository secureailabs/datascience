from typing import Tuple

import pytest
from sail_safe_functions_orchestrator import statistics
from sail_safe_functions_orchestrator.statistics.chisquare import Chisquare
from sail_safe_functions_test.helper_sail_safe_functions.series_federated_local import (
    SeriesFederatedLocal,
)


@pytest.mark.active
def test_chisquare_direct(
    two_sample_categorical: Tuple[SeriesFederatedLocal, SeriesFederatedLocal]
):
    """
    This is our test for the Sails federated chisquare test

    :param two_sample_categorical a dataset with cathegorical data
    :type two_sample_categorical: Tuple[SeriesFederatedLocal, SeriesFederatedLocal]
    """
    # Arrange
    sample_0 = two_sample_categorical[0]
    sample_1 = two_sample_categorical[1]

    # Act
    statistics.chisquare(sample_0, sample_1)


@pytest.mark.active
def test_chisquare(
    two_sample_categorical: Tuple[SeriesFederatedLocal, SeriesFederatedLocal]
):
    """
    This is our test for the Sails federated chisquare test

    :param two_sample_categorical a dataset with cathegorical data
    :type two_sample_categorical: Tuple[SeriesFederatedLocal, SeriesFederatedLocal]
    """
    # Arrange
    sample_0 = two_sample_categorical[0]
    sample_1 = two_sample_categorical[1]

    # Act
    estimator = Chisquare()
    pearson_sail, p_value_sail = estimator.Run(sample_0, sample_1)
    pearson_scipy, p_value_scipy = estimator.run_reference(sample_0, sample_1)

    # Assert
    assert pearson_scipy == pytest.approx(pearson_sail, 0.0001)
    assert p_value_scipy == pytest.approx(p_value_sail, 0.0001)
