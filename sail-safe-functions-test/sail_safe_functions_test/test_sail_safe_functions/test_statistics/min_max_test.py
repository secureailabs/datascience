from typing import Tuple

import pytest
from sail_safe_functions_orchestrator.statistics.min_max import MinMax
from sail_safe_functions_test.helper_sail_safe_functions.data_frame_federated_local import DataFrameFederatedLocal
from sail_safe_functions_test.helper_sail_safe_functions.series_federated_local import SeriesFederatedLocal


@pytest.mark.active
def test_min_max(one_sample_big: SeriesFederatedLocal):
    """This test our federated min max function

    :param one_sample_big: A single federated series fixture
    :type one_sample_big: SeriesFederatedLocal
    """

    # Arrange
    sample_0 = one_sample_big

    # Act
    estimator = MinMax()
    min_sail, max_sail = estimator.run(sample_0)
    min_numpy, max_numpy = estimator.run_reference(sample_0)

    # Assert
    assert max_numpy <= max_sail
    assert min_numpy >= min_sail


@pytest.mark.active
def test_min_max_kidney(tuple_kidney_schema_dataframe: Tuple[dict, DataFrameFederatedLocal]):
    """This test our federated min max function with the clean kidney dataset

    :param one_sample_big: A single federated data_frame_federated_kidney fixture
    :type one_sample_big: SeriesFederatedLocal
    """

    # Arrange
    sample_0 = tuple_kidney_schema_dataframe[1]["age"]

    # Act
    estimator = MinMax()
    min_sail, max_sail = estimator.run(sample_0)
    min_numpy, max_numpy = estimator.run_reference(sample_0)

    # Assert
    assert min_numpy >= min_sail
    assert max_numpy <= max_sail
