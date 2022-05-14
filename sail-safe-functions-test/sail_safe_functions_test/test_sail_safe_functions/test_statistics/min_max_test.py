import pytest
from sail_safe_functions_orchestrator.statistics.min_max_federate import MinMaxFederate
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
    # Calling fedrated sail skewness method
    min_sail, max_sail = MinMaxFederate.Run(sample_0)
    min_numpy, max_numpy = MinMaxFederate.RunReference(sample_0)

    # Assert
    assert max_numpy <= max_sail
    assert min_numpy >= min_sail
