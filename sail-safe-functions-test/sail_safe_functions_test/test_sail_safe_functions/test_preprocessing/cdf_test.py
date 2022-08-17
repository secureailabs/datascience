from typing import Tuple

import pandas
from sail_safe_functions_orchestrator import preprocessing
from sail_safe_functions_test.helper_sail_safe_functions.data_frame_federated_local import DataFrameFederatedLocal


@pytest.mark.active
def test_binary():
    """This test our federated min max function with the clean kidney dataset

    :param one_sample_big: A single federated data_frame_federated_kidney fixture
    :type one_sample_big: SeriesFederatedLocal
    """

    # Arrange
