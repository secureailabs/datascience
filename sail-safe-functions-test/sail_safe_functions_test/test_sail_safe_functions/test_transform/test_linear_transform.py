import os

import numpy
import pandas
import pytest
from sail_safe_functions_orchestrator.data_frame_federated import DataFrameFederated
from sail_safe_functions_orchestrator.service_reference import ServiceReference
from sail_safe_functions_orchestrator.transform.linear import Linear
from sail_safe_functions_test.helper_sail_safe_functions.data_frame_federated_local import DataFrameFederatedLocal


@pytest.mark.active
def test_series_count(data_frame_federated_house: DataFrameFederated):
    """
    This is test to found the number of columns/series are right

    """
    arrray_transform = numpy.zeros((2, 2))
    arrray_transform[0, 0] = 1
    arrray_transform[1, 1] = 1
    arrray_transform[0, 1] = 1
    datasource = data_frame_federated_house
    transform = Linear()
    datasource_transformed = transform.run(datasource, arrray_transform, ["households"], ["households2"], False)
    refernce_datasource = list(datasource_transformed.dict_reference_data_frame.values())[0]

    datasource_final = ServiceReference.get_instance().reference_to_data_frame(refernce_datasource)

    assert 1 == len(datasource_final.list_series_name)


@pytest.mark.active
def test_identity_matrix(data_frame_federated_house: DataFrameFederated):
    """
    This is test to verify that linear transform returns same value with identity matrix

    """
    arrray_transform = numpy.zeros((2, 2))
    arrray_transform[0, 0] = 1
    arrray_transform[1, 1] = 1

    datasource = data_frame_federated_house
    transform = Linear()
    datasource_transformed = transform.run(datasource, arrray_transform, ["households"], ["households2"], False)
    refernce_datasource = list(datasource_transformed.dict_reference_data_frame.values())[0]

    datasource_final = ServiceReference.get_instance().reference_to_data_frame(refernce_datasource)
    array_source = datasource["households"].to_numpy().astype(numpy.float64)
    array_target = datasource_final["households2"].to_numpy().astype(numpy.float64)

    assert numpy.allclose(array_source, array_target)


@pytest.mark.active
def test_twice_matrix(data_frame_federated_house: DataFrameFederated):
    """
    This is test to verify that linear transform with twice matrix

    """
    arrray_transform = numpy.zeros((2, 2))
    arrray_transform[0, 0] = 2
    datasource = data_frame_federated_house
    transform = Linear()
    datasource_transformed = transform.run(datasource, arrray_transform, ["households"], ["households2"], False)
    refernce_datasource = list(datasource_transformed.dict_reference_data_frame.values())[0]

    datasource_final = ServiceReference.get_instance().reference_to_data_frame(refernce_datasource)
    array_source = datasource["households"].to_numpy().astype(numpy.float64)
    array_target = datasource_final["households2"].to_numpy().astype(numpy.float64)

    assert array_source[0] == array_target[0] / 2
    assert array_source[5] == array_target[5] / 2
    assert array_source[12] == array_target[12] / 2
    assert array_source[26] == array_target[26] / 2


@pytest.mark.active
def test_inverse(data_frame_federated_house: DataFrameFederated):
    """
    This is test to find the inverse is working and working with multiple columns

    """
    array_transform = numpy.zeros((4, 4))
    array_transform[0, 0] = 2
    array_transform[1, 1] = 2
    array_transform[2, 2] = 2
    array_transform[3, 3] = 1
    array_transform[0, 3] = 1
    array_transform[1, 3] = 1
    array_transform[2, 3] = 1

    list1 = ["households", "median_income", "median_house_value"]
    list2 = ["households1", "median_income1", "median_house_value1"]
    datasource = data_frame_federated_house
    transform = Linear()
    datasource_transformed = transform.run(datasource, array_transform, list1, list2, False)
    datasource_transformed_inverse = transform.run(datasource_transformed, array_transform, list2, list1, True)

    reference_dataframe_transformed_inv = list(datasource_transformed_inverse.dict_reference_data_frame.values())[0]

    transformed_numpy_inv = ServiceReference.get_instance().reference_to_data_frame(reference_dataframe_transformed_inv)  # type: ignore
    array_transformed_inv = transformed_numpy_inv.to_numpy().astype(numpy.float64)
    reference_datasource = list(datasource.dict_reference_data_frame.values())[0]
    datasource_final = ServiceReference.get_instance().reference_to_data_frame(reference_datasource)
    array_source_ini = datasource_final.select_series(list1).to_numpy().astype(numpy.float64)
    assert numpy.allclose(array_transformed_inv, array_source_ini)
