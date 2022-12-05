import os

import numpy
import pandas
import pytest
from sail_safe_functions_orchestrator.data_frame_federated import DataFrameFederated
from sail_safe_functions_orchestrator.service_reference import ServiceReference
from sail_safe_functions_orchestrator.transform.linear import Linear
from sail_safe_functions_test.helper_sail_safe_functions.data_frame_federated_local import DataFrameFederatedLocal


@pytest.mark.active
def test_series_count():
    """
    This is test to found the number of columns/series are right

    """
    array_try = numpy.zeros((2, 2))
    array_try[0, 0] = 1
    array_try[1, 1] = 1
    array_try[0, 1] = 1
    path = os.path.join(os.getcwd(), "sail_safe_functions_test/data_sail_safe_functions/california_housing_train.csv")
    Datasource = DataFrameFederatedLocal.from_csv({"dataset_0": path})
    transform = Linear()
    ans = transform.run(Datasource, array_try, ["households"], ["households2"], False)
    ans_2 = list(ans.dict_reference_data_frame.values())[0]

    new = ServiceReference.get_instance().reference_to_data_frame(ans_2)

    assert len(Datasource.list_series_name) + 1 == len(new.list_series_name)


@pytest.mark.active
def test_identity_matrix():
    """
    This is test to verify that linear transform returns same value with identity matrix

    """
    array_try = numpy.zeros((2, 2))
    array_try[0, 0] = 1
    array_try[1, 1] = 1
    array_try[0, 1] = 0
    path = os.path.join(os.getcwd(), "sail_safe_functions_test/data_sail_safe_functions/california_housing_train.csv")
    Datasource = DataFrameFederatedLocal.from_csv({"dataset_0": path})
    transform = Linear()
    ans = transform.run(Datasource, array_try, ["households"], ["households2"], False)
    ans_2 = list(ans.dict_reference_data_frame.values())[0]

    new = ServiceReference.get_instance().reference_to_data_frame(ans_2)
    array_source = Datasource["households"].to_numpy().astype(numpy.float64)
    array_target = new["households2"].to_numpy().astype(numpy.float64)

    assert array_source[0] == array_target[0]
    assert array_source[5] == array_target[5]
    assert array_source[12] == array_target[12]
    assert array_source[26] == array_target[26]


@pytest.mark.active
def test_twice_matrix():
    """
    This is test to verify that linear transform with twice matrix

    """
    array_try = numpy.zeros((2, 2))
    array_try[0, 0] = 2
    array_try[1, 1] = 0
    array_try[0, 1] = 0
    path = os.path.join(os.getcwd(), "sail_safe_functions_test/data_sail_safe_functions/california_housing_train.csv")
    Datasource = DataFrameFederatedLocal.from_csv({"dataset_0": path})
    transform = Linear()
    ans = transform.run(Datasource, array_try, ["households"], ["households2"], False)
    ans_2 = list(ans.dict_reference_data_frame.values())[0]

    new = ServiceReference.get_instance().reference_to_data_frame(ans_2)
    array_source = Datasource["households"].to_numpy().astype(numpy.float64)
    array_target = new["households2"].to_numpy().astype(numpy.float64)

    assert array_source[0] == array_target[0] / 2
    assert array_source[5] == array_target[5] / 2
    assert array_source[12] == array_target[12] / 2
    assert array_source[26] == array_target[26] / 2
