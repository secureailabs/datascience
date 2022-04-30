import pandas as pd
import pytest
from sail_safe_functions.preprocessing.impute_constant import ImputeConstant


@pytest.mark.active
def test_age_happy(dataframe_kidney: pd.DataFrame):
    """Test if the 9 nan in the age column get repaced by ones

    :param dataframe_kidney: a dataframe with nans
    :type dataframe_kidney: pd.DataFrame
    """
    # Arrange

    # Act
    dataframe_kidney_fixed = ImputeConstant.Run(dataframe_kidney, list_name_column=["age"], missing_value=0)

    # Assert
    assert 9 == dataframe_kidney["age"].isna().sum()
    assert 0 == dataframe_kidney_fixed["age"].isna().sum()


@pytest.mark.active
def test_age_exception(dataframe_kidney: pd.DataFrame):
    """Test if the string insertion gets rejected

    :param dataframe_kidney: a dataframe with nans
    :type dataframe_kidney: pd.DataFrame
    """
    # Arrange

    # Act
    with pytest.raises(ValueError, match="missing_value is string type but column with name age is not"):
        ImputeConstant.Run(dataframe_kidney, list_name_column=["age"], missing_value="stringvalue")

    # Assert


@pytest.mark.active
def test_rbc_happy(dataframe_kidney: pd.DataFrame):
    """Test if the 152 nan in the `rbc` column get repaced by "normal"

    :param dataframe_kidney: a dataframe with nans
    :type dataframe_kidney: pd.DataFrame
    """
    # Arrange

    # Act
    dataframe_kidney_fixed = ImputeConstant.Run(dataframe_kidney, list_name_column=["rbc"], missing_value="normal")

    # Assert
    assert 152 == dataframe_kidney["rbc"].isna().sum()
    assert 0 == dataframe_kidney_fixed["rbc"].isna().sum()


@pytest.mark.active
def test_rbc_exception(dataframe_kidney: pd.DataFrame):
    """Test if the string insertion gets rejected

    :param dataframe_kidney: a dataframe with nans
    :type dataframe_kidney: pd.DataFrame
    """
    # Arrange

    # Act
    with pytest.raises(ValueError, match="missing_value is numeric type but column with name rbc is not"):
        ImputeConstant.Run(dataframe_kidney, list_name_column=["rbc"], missing_value=0)

    # Assert


@pytest.mark.active
def test_rbc_pc_happy(dataframe_kidney: pd.DataFrame):
    """Test if the nan in the `rbc` and `pc` column get repaced by "normal"

    :param dataframe_kidney: a dataframe with nans
    :type dataframe_kidney: pd.DataFrame
    """
    # Arrange

    # Act
    dataframe_kidney_fixed = ImputeConstant.Run(
        dataframe_kidney, list_name_column=["rbc", "pc"], missing_value="normal"
    )

    # Assert
    assert 152 == dataframe_kidney["rbc"].isna().sum()
    assert 0 == dataframe_kidney_fixed["rbc"].isna().sum()
    assert 65 == dataframe_kidney["pc"].isna().sum()
    assert 0 == dataframe_kidney_fixed["pc"].isna().sum()
