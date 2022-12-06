import json

import pytest
from sail_safe_functions_orchestrator import visualization
from sail_safe_functions_orchestrator.data_frame_federated import \
    DataFrameFederated


@pytest.mark.active
def test_kernel_density_estimation(data_frame_federated_kidney: DataFrameFederated):
    """
    This test only checks if the function completes and if the result is json-serializable
    """
    # Arrange
    sample_0 = data_frame_federated_kidney["age"]

    # Act
    fig_dict = visualization.kernel_density_estimation(sample_0, 0.6)
    json.dumps(fig_dict)
