import pandas as pd
import pytest
from sail_safe_functions.preprocessing.impute_multivariate import ImputeMultivariate


@pytest.mark.active
def test_exception(dataframe_kidney: pd.DataFrame):
    """Test if the imputation_order parameter gets checked

    :param dataframe_kidney: a dataframe with nans
    :type dataframe_kidney: pd.DataFrame
    """
    # Arrange

    # Act
    with pytest.raises(ValueError, match="`imputation_order` must be either in {`ascending`, `descending`}"):
        dataframe_kidney_fixed = ImputeMultivariate.Run(
            dataframe_kidney, list_name_column=["age"], imputation_order="nope"
        )

    # Assert


@pytest.mark.active
def test_age(dataframe_kidney: pd.DataFrame):
    """Test if the 9 nan in the age column get repaced by multivariate estimation

    :param dataframe_kidney: a dataframe with nans
    :type dataframe_kidney: pd.DataFrame
    """
    # Arrange

    # Act
    dataframe_kidney_fixed = ImputeMultivariate.Run(
        dataframe_kidney, list_name_column=["age"], imputation_order="ascending"
    )

    # Assert
    assert 9 == dataframe_kidney["age"].isna().sum()
    assert 0 == dataframe_kidney_fixed["age"].isna().sum()
    assert pytest.approx(20130.0, 0.0001) == dataframe_kidney["age"].sum()
    assert pytest.approx(20604.530413505294, 0.0001) == dataframe_kidney_fixed["age"].sum()


@pytest.mark.active
def test_rbc(dataframe_kidney: pd.DataFrame):
    """Test if the 152 nan in the `rbc` column get repaced by "most_frequent"

    :param dataframe_kidney: a dataframe with nans
    :type dataframe_kidney: pd.DataFrame
    """
    # Arrange

    # Act
    dataframe_kidney_fixed = ImputeMultivariate.Run(
        dataframe_kidney, list_name_column=["rbc"], imputation_order="ascending"
    )

    # Assert
    assert 152 == dataframe_kidney["rbc"].isna().sum()
    assert 0 == dataframe_kidney_fixed["rbc"].isna().sum()


@pytest.mark.active
def test_all(dataframe_kidney: pd.DataFrame):
    """Test if all the nan in the dataframe get repaced

    :param dataframe_kidney: a dataframe with nans
    :type dataframe_kidney: pd.DataFrame
    """
    # Arrange

    # Act
    dataframe_kidney_fixed = ImputeMultivariate.Run(
        dataframe_kidney, list_name_column=None, imputation_order="ascending"
    )

    # Assert
    assert 152 == dataframe_kidney["rbc"].isna().sum()
    assert 65 == dataframe_kidney["pc"].isna().sum()
    assert 9 == dataframe_kidney["age"].isna().sum()

    for name_column in dataframe_kidney_fixed.columns:
        assert 0 == dataframe_kidney_fixed[name_column].isna().sum()

    assert pytest.approx(20130.0, 0.0001) == dataframe_kidney["age"].sum()
    assert pytest.approx(20604.530413505294, 0.0001) == dataframe_kidney_fixed["age"].sum()
