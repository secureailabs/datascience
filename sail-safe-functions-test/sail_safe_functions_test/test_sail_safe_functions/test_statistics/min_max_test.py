import pytest
from sail_safe_functions_orchestrator.statistics.min_max import MinMax
from sail_safe_functions_test.helper_sail_safe_functions.series_federated_local import SeriesFederatedLocal


@pytest.mark.active
def test_min_max(one_sample_big: SeriesFederatedLocal):
    """This test our federated Skewness module

    :param one_sample_big: A single federated series fixture
    :type one_sample_big: SeriesFederatedLocal
    """

    # Arrange
    sample_0 = one_sample_big

    # Act
    estimator = MinMax()
    min_sail, max_sail = estimator.Run(sample_0)
    min_numpy, max_numpy = estimator.run_reference(sample_0)

    # Assert
    assert max_numpy <= max_sail
    assert min_numpy >= min_sail
