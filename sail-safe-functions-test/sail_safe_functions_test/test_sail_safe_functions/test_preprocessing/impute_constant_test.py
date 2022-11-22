import pytest
from sail_safe_functions_orchestrator import preprocessing
from sail_safe_functions_orchestrator.data_frame_federated import DataFrameFederated
from sail_safe_functions_orchestrator.service_reference import ServiceReference


@pytest.mark.active
def test_age_happy(data_frame_federated_kidney_hasnan: DataFrameFederated):
    """Test if the 9 nan in the age column get repaced by ones

    :param data_frame_federated_kidney: a dataframe with nans
    :type dataframe_kidney: DataFrameFederated
    """
    # Arrange

    # Act
    data_frame_federated_kidney_fixed = preprocessing.impute_constant(
        data_frame_federated_kidney_hasnan, list_name_column=["age"], missing_value=0
    )
    reference_data_frame_kidney_fixed = list(data_frame_federated_kidney_fixed.dict_reference_data_frame.values())[0]
    reference_data_frame_kidney = list(data_frame_federated_kidney_hasnan.dict_reference_data_frame.values())[0]
    data_frame_kidney_fixed = ServiceReference.get_instance().reference_to_data_frame(reference_data_frame_kidney_fixed)
    data_frame_kidney = ServiceReference.get_instance().reference_to_data_frame(reference_data_frame_kidney)

    # Assert
    assert 9 == data_frame_kidney["age"].isna().sum()
    assert 0 == data_frame_kidney_fixed["age"].isna().sum()


@pytest.mark.active
def test_age_exception(data_frame_federated_kidney_hasnan: DataFrameFederated):
    """Test if the string insertion gets rejected

    :param data_frame_federated_kidney: a dataframe with nans
    :type dataframe_kidney: DataFrameFederated
    """
    # Arrange

    # Act
    with pytest.raises(ValueError, match="missing_value is string type but series with series_name age is not"):
        preprocessing.impute_constant(
            data_frame_federated_kidney_hasnan, list_name_column=["age"], missing_value="stringvalue"
        )

    # Assert


@pytest.mark.active
def test_rbc_happy(data_frame_federated_kidney_hasnan: DataFrameFederated):
    """Test if the 152 nan in the `rbc` column get repaced by "normal"

    :param data_frame_federated_kidney: a dataframe with nans
    :type dataframe_kidney: DataFrameFederated
    """
    # Arrange

    # Act
    data_frame_federated_kidney_fixed = preprocessing.impute_constant(
        data_frame_federated_kidney_hasnan, list_name_column=["rbc"], missing_value="normal"
    )
    reference_data_frame_kidney_fixed = list(data_frame_federated_kidney_fixed.dict_reference_data_frame.values())[0]
    reference_data_frame_kidney = list(data_frame_federated_kidney_hasnan.dict_reference_data_frame.values())[0]
    data_frame_kidney_fixed = ServiceReference.get_instance().reference_to_data_frame(reference_data_frame_kidney_fixed)
    data_frame_kidney = ServiceReference.get_instance().reference_to_data_frame(reference_data_frame_kidney)

    # Assert
    assert 152 == data_frame_kidney["rbc"].isna().sum()
    assert 0 == data_frame_kidney_fixed["rbc"].isna().sum()


@pytest.mark.active
def test_rbc_exception(data_frame_federated_kidney_hasnan: DataFrameFederated):
    """Test if the string insertion gets rejected

    :param data_frame_federated_kidney: a dataframe with nans
    :type dataframe_kidney: DataFrameFederated
    """
    # Arrange

    # Act
    with pytest.raises(ValueError, match="missing_value is numeric type but series with series_name rbc is not"):
        preprocessing.impute_constant(data_frame_federated_kidney_hasnan, list_name_column=["rbc"], missing_value=0)

    # Assert


@pytest.mark.active
def test_rbc_pc_happy(data_frame_federated_kidney_hasnan: DataFrameFederated):
    """Test if the nan in the `rbc` and `pc` column get repaced by "normal"

    :param dataframe_kidney: a dataframe with nans
    :type dataframe_kidney: pd.DataFrame
    """
    # Arrange

    # Act
    data_frame_federated_kidney_fixed = preprocessing.impute_constant(
        data_frame_federated_kidney_hasnan, list_name_column=["rbc", "pc"], missing_value="normal"
    )
    reference_data_frame_kidney_fixed = list(data_frame_federated_kidney_fixed.dict_reference_data_frame.values())[0]
    reference_data_frame_kidney = list(data_frame_federated_kidney_hasnan.dict_reference_data_frame.values())[0]
    data_frame_kidney_fixed = ServiceReference.get_instance().reference_to_data_frame(reference_data_frame_kidney_fixed)
    data_frame_kidney = ServiceReference.get_instance().reference_to_data_frame(reference_data_frame_kidney)

    # Assert
    assert 152 == data_frame_kidney["rbc"].isna().sum()
    assert 0 == data_frame_kidney_fixed["rbc"].isna().sum()
    assert 65 == data_frame_kidney["pc"].isna().sum()
    assert 0 == data_frame_kidney_fixed["pc"].isna().sum()
