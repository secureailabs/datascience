import os

import numpy
import pandas
import pytest
from sail_safe_functions_orchestrator.data_frame_federated import DataFrameFederated
from sail_safe_functions_orchestrator.service_reference import ServiceReference
from sail_safe_functions_orchestrator.transform.scaling_min_max import ScalingMinMax
from sail_safe_functions_test.helper_sail_safe_functions.data_frame_federated_local import DataFrameFederatedLocal


@pytest.mark.active
def test_series_count_min_max(data_frame_federated_house):
    """
    This is test to found the number of columns/series are right

    """
    datasource = data_frame_federated_house
    transform = ScalingMinMax()
    transformed = transform.run(datasource, ["households"], ["households2"], [0, 1], False)
    reference_transformed = list(transformed.dict_reference_data_frame.values())[0]

    final_datasource = ServiceReference.get_instance().reference_to_data_frame(reference_transformed)

    assert 1 == len(final_datasource.list_series_name)


@pytest.mark.active
def test_values(data_frame_federated_house):
    """
    This is test to verify that after transform values lies between zero and one

    """
    datasource = data_frame_federated_house
    transform = ScalingMinMax()
    transformed = transform.run(datasource, ["households"], ["households2"], [0, 1], False)
    reference_transformed = list(transformed.dict_reference_data_frame.values())[0]

    final_datasource = ServiceReference.get_instance().reference_to_data_frame(reference_transformed)

    array_target = final_datasource["households2"].to_numpy().astype(numpy.float64)
    for i in range(len(array_target)):
        assert 0 <= array_target[i] <= 1
