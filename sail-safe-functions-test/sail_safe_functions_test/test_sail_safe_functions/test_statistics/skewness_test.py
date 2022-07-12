import pytest
from sail_safe_functions_orchestrator.statistics.skewness import Skewness
from sail_safe_functions_test.helper_sail_safe_functions.series_federated_local import SeriesFederatedLocal
from scipy import stats


@pytest.mark.active
def test_skewness(one_sample_big: SeriesFederatedLocal):
    """This test our federated Skewness module

    :param one_sample_big: A single federated series fixture
    :type one_sample_big: SeriesFederatedLocal
    """

    # Arrange
    sample_0 = one_sample_big

    # Act
    estimator = Skewness()
    skewness_sail = estimator.run(sample_0)
    skewness_scipy = estimator.run_reference(sample_0)

    # Assert
    assert skewness_scipy == pytest.approx(skewness_sail, 0.0001)
