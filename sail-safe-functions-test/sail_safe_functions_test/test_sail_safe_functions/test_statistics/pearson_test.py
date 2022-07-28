from typing import Tuple

import pytest
from sail_safe_functions_orchestrator.statistics.pearson import Pearson
from sail_safe_functions_test.helper_sail_safe_functions.series_federated_local import (
    SeriesFederatedLocal,
)
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
    alternative = "two-sided"

    # Act
    estimator = Pearson(alternative=alternative)
    pearson_sail, p_value_sail = estimator.run(sample_0, sample_1)
    pearson_scipy, p_value_scipy = estimator.run_reference(sample_0, sample_1)

    # Assert
    assert pearson_scipy == pytest.approx(pearson_sail, 0.0001)
    assert p_value_scipy == pytest.approx(p_value_sail, 0.0001)
