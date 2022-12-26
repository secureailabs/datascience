import json

import pytest
from sail_safe_functions.aggregator import visualization
from sail_safe_functions.aggregator.data_frame_federated import DataFrameFederated


@pytest.mark.active
def test_kernel_density_estimation(data_frame_federated_kidney: DataFrameFederated):
    """
    This test only checks if the function completes and if the result is json-serializable
    """
    # Arrange
    sample_0 = data_frame_federated_kidney["age"]

    # Act
    fig_dict = visualization.histogram_federated(sample_0, 20)
    json.dumps(fig_dict)
