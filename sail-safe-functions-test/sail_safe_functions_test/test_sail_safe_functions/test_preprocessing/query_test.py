import pandas as pd
import pytest
from sail_safe_functions_orchestrator import preprocessing
from sail_safe_functions_orchestrator.data_frame_federated import DataFrameFederated
from sail_safe_functions_orchestrator.service_reference import ServiceReference


@pytest.mark.active
def test_comparison_on_constant(data_frame_federated_kidney: DataFrameFederated):
    """
    Tests comparison with constant query

        :param dataframe_kidney: a dataframe with nans
        :type: pd.DataFrame

        :param data_frame_federated_kidney: a dataframe with nans
        :type dataframe_kidney: DataFrameFederated
    """
    # Arrange
    query = "pcc == 'notpresent'"

    # Act
    data_frame_federated_result = preprocessing.query(data_frame_federated_kidney, query)
    reference_data_frame_kidney = list(data_frame_federated_kidney.dict_reference_data_frame.values())[0]
    reference_data_frame_result = list(data_frame_federated_result.dict_reference_data_frame.values())[0]
    data_frame_kidney = ServiceReference.get_instance().reference_to_data_frame(reference_data_frame_kidney)
    data_frame_result = ServiceReference.get_instance().reference_to_data_frame(reference_data_frame_result)
    data_frame_result_direct = data_frame_kidney.query(query)

    # Assert
    assert data_frame_result.equals(data_frame_result_direct)


@pytest.mark.active
def test_comparison_on_columns(data_frame_federated_kidney: DataFrameFederated):
    """
    Tests comparison with column query

        :param dataframe_kidney: a dataframe with nans
        :type: pd.DataFrame

        :param data_frame_federated_kidney: a dataframe with nans
        :type dataframe_kidney: DataFrameFederated
    """
    # Arrange
    query = "sg < al"

    # Act
    data_frame_federated_result = preprocessing.query(data_frame_federated_kidney, query)
    reference_data_frame_kidney = list(data_frame_federated_kidney.dict_reference_data_frame.values())[0]
    reference_data_frame_result = list(data_frame_federated_result.dict_reference_data_frame.values())[0]
    data_frame_kidney = ServiceReference.get_instance().reference_to_data_frame(reference_data_frame_kidney)
    data_frame_result = ServiceReference.get_instance().reference_to_data_frame(reference_data_frame_result)
    data_frame_result_direct = data_frame_kidney.query(query)

    # Assert
    assert data_frame_result.equals(data_frame_result_direct)


@pytest.mark.active
def test_comparison_on_variable(data_frame_federated_kidney: DataFrameFederated):
    """
    Tests comparison with variable query

        :param dataframe_kidney: a dataframe with nans
        :type: pd.DataFrame

        :param data_frame_federated_kidney: a dataframe with nans
        :type dataframe_kidney: DataFrameFederated
    """
    # Arrange
    min_age, max_age = 18, 25

    query = "@min_age <= age <= @max_age"

    # Act
    data_frame_federated_result = preprocessing.query(data_frame_federated_kidney, query)
    reference_data_frame_kidney = list(data_frame_federated_kidney.dict_reference_data_frame.values())[0]
    reference_data_frame_result = list(data_frame_federated_result.dict_reference_data_frame.values())[0]
    data_frame_kidney = ServiceReference.get_instance().reference_to_data_frame(reference_data_frame_kidney)
    data_frame_result = ServiceReference.get_instance().reference_to_data_frame(reference_data_frame_result)
    data_frame_result_direct = data_frame_kidney.query(query)

    # Assert
    assert data_frame_result.equals(data_frame_result_direct)


@pytest.mark.active
def test_unauthorized_var_type(
    data_frame_federated_kidney: DataFrameFederated,
):
    """
    Tests that environment gets sanitized properly

        :param data_frame_federated_kidney: a dataframe with nans
        :type data_frame_federated_kidney: DataFrameFederated
    """

    # Arrange
    def forbidden_type_var():
        print("arbitrary code")

    query = "age == @forbidden_type_var"

    # Act
    with pytest.raises(
        pd.core.computation.ops.UndefinedVariableError,
        match="local variable 'forbidden_type_var' is not defined",
    ):
        preprocessing.query(data_frame_federated_kidney, query)

    # Assert


@pytest.mark.active
def test_object_attribute(
    data_frame_federated_kidney: DataFrameFederated,
):
    """
    Tests that we can't access attributes
    (it would be extremely inneficient to go check all the attributes of all the variables in the env,
    if the user wants to use the attribute of an objet they have to assign it to a variable so we can check it)
    (This will be more useful when/if we start allowing more variables types)

        :param data_frame_federated_kidney: a dataframe with nans
        :type data_frame_federated_kidney: DataFrameFederated
    """

    # Arrange
    string_var = "string of length 19"

    query = "@string_var.partition"

    # Act
    with pytest.raises(
        ValueError,
        match="Invalid query",
    ):
        preprocessing.query(data_frame_federated_kidney, query)
