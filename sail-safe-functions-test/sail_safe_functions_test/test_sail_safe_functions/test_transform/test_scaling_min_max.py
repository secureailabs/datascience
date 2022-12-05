import os

import numpy
import pandas
import pytest
from sail_safe_functions_orchestrator.data_frame_federated import DataFrameFederated
from sail_safe_functions_orchestrator.service_reference import ServiceReference
from sail_safe_functions_orchestrator.transform.scaling_min_max import ScalingMinMax
from sail_safe_functions_test.helper_sail_safe_functions.data_frame_federated_local import DataFrameFederatedLocal


@pytest.mark.active
def test_series_count_min_max():
    """
    This is test to found the number of columns/series are right

    """
    path = os.path.join(os.getcwd(), "sail_safe_functions_test/data_sail_safe_functions/california_housing_train.csv")
    Datasource = DataFrameFederatedLocal.from_csv({"dataset_0": path})
    transform = ScalingMinMax()
    ans = transform.run(Datasource, ["households"], ["households2"], [0, 1], False)
    ans_2 = list(ans.dict_reference_data_frame.values())[0]

    new = ServiceReference.get_instance().reference_to_data_frame(ans_2)

    assert len(Datasource.list_series_name) + 1 == len(new.list_series_name)


@pytest.mark.active
def test_values():
    """
    This is test to verify that after transform values lies between zero and one

    """

    path = os.path.join(os.getcwd(), "sail_safe_functions_test/data_sail_safe_functions/california_housing_train.csv")
    Datasource = DataFrameFederatedLocal.from_csv({"dataset_0": path})
    transform = ScalingMinMax()
    ans = transform.run(Datasource, ["households"], ["households2"], [0, 1], False)
    ans_2 = list(ans.dict_reference_data_frame.values())[0]

    new = ServiceReference.get_instance().reference_to_data_frame(ans_2)
    array_source = Datasource["households"].to_numpy().astype(numpy.float64)
    array_target = new["households2"].to_numpy().astype(numpy.float64)

    assert 0 <= array_target[0] <= 1
    assert 0 <= array_target[5] <= 1
    assert 0 <= array_target[10] <= 1
    assert 0 <= array_target[20] <= 1
