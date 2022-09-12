import pandas as pd
import pytest
from sail_safe_functions_orchestrator import preprocessing
from sail_safe_functions_orchestrator.data_frame_federated import DataFrameFederated


@pytest.mark.active
def test_comparison_on_constant(dataframe_kidney: pd.DataFrame, data_frame_federated_kidney: DataFrameFederated):
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
    federated_dataframe_result = preprocessing.query(data_frame_federated_kidney, query)
    pd_dataframe_result = list(federated_dataframe_result.dict_dataframe.values())[0]

    # Assert
    assert dataframe_kidney.query(query).equals(pd_dataframe_result)


@pytest.mark.active
def test_comparison_on_columns(dataframe_kidney: pd.DataFrame, data_frame_federated_kidney: DataFrameFederated):
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
    federated_dataframe_result = preprocessing.query(data_frame_federated_kidney, query)
    pd_dataframe_result = list(federated_dataframe_result.dict_dataframe.values())[0]

    # Assert
    assert dataframe_kidney.query(query).equals(pd_dataframe_result)


@pytest.mark.active
def test_comparison_on_variable(dataframe_kidney: pd.DataFrame, data_frame_federated_kidney: DataFrameFederated):
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
    federated_dataframe_result = preprocessing.query(data_frame_federated_kidney, query)
    pd_dataframe_result = list(federated_dataframe_result.dict_dataframe.values())[0]

    # Assert
    assert dataframe_kidney.query(query).equals(pd_dataframe_result)


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
