import pandas as pd
import pytest
from sail_safe_functions.preprocessing.impute_univariate import ImputeUnivariate


@pytest.mark.active
def test_age_exception(dataframe_kidney: pd.DataFrame):
    """Test if the strategy parameter gets checked

    :param dataframe_kidney: a dataframe with nans
    :type dataframe_kidney: pd.DataFrame
    """
    # Arrange

    # Act
    with pytest.raises(ValueError, match="parameter `strategy` must be either mean, median or most_frequent"):
        dataframe_kidney_fixed = ImputeUnivariate.Run(dataframe_kidney, list_name_column=["age"], strategy="nope")

    # Assert


@pytest.mark.active
def test_age_mean(dataframe_kidney: pd.DataFrame):
    """Test if the 9 nan in the age column get repaced by mean

    :param dataframe_kidney: a dataframe with nans
    :type dataframe_kidney: pd.DataFrame
    """
    # Arrange

    # Act
    dataframe_kidney_fixed = ImputeUnivariate.Run(dataframe_kidney, list_name_column=["age"], strategy="mean")

    # Assert
    assert 9 == dataframe_kidney["age"].isna().sum()
    assert 0 == dataframe_kidney_fixed["age"].isna().sum()
    assert pytest.approx(20130.0, 0.0001) == dataframe_kidney["age"].sum()
    assert pytest.approx(20593.35038363171, 0.0001) == dataframe_kidney_fixed["age"].sum()


@pytest.mark.active
def test_age_median(dataframe_kidney: pd.DataFrame):
    """Test if the 9 nan in the age column get repaced by median

    :param dataframe_kidney: a dataframe with nans
    :type dataframe_kidney: pd.DataFrame
    """
    # Arrange

    # Act
    dataframe_kidney_fixed = ImputeUnivariate.Run(dataframe_kidney, list_name_column=["age"], strategy="median")

    # Assert
    assert 9 == dataframe_kidney["age"].isna().sum()
    assert 0 == dataframe_kidney_fixed["age"].isna().sum()
    assert pytest.approx(20130.0, 0.0001) == dataframe_kidney["age"].sum()
    assert pytest.approx(20625.0, 0.0001) == dataframe_kidney_fixed["age"].sum()


@pytest.mark.active
def test_age_most_frequent(dataframe_kidney: pd.DataFrame):
    """Test if the string insertion gets rejected

    :param dataframe_kidney: a dataframe with nans
    :type dataframe_kidney: pd.DataFrame
    """
    # Arrange

    # Act
    dataframe_kidney_fixed = ImputeUnivariate.Run(dataframe_kidney, list_name_column=["age"], strategy="most_frequent")

    # Assert
    assert 9 == dataframe_kidney["age"].isna().sum()
    assert 0 == dataframe_kidney_fixed["age"].isna().sum()
    assert pytest.approx(20130.0, 0.0001) == dataframe_kidney["age"].sum()
    assert pytest.approx(20670.0, 0.0001) == dataframe_kidney_fixed["age"].sum()


@pytest.mark.active
def test_rbc_exception(dataframe_kidney: pd.DataFrame):
    """Test if the 152 nan in the `rbc` column raise an exception when mean is used

    :param dataframe_kidney: a dataframe with nans
    :type dataframe_kidney: pd.DataFrame
    """
    # Arrange

    # Act
    with pytest.raises(
        ValueError,
        match="`mean`, `median` strategies cannot not operate on column with name rbc which is of string type",
    ):
        dataframe_kidney_fixed = ImputeUnivariate.Run(dataframe_kidney, list_name_column=["rbc"], strategy="mean")

    # Assert


@pytest.mark.active
def test_rbc_most_frequent(dataframe_kidney: pd.DataFrame):
    """Test if the 152 nan in the `rbc` column get repaced by "most_frequent"

    :param dataframe_kidney: a dataframe with nans
    :type dataframe_kidney: pd.DataFrame
    """
    # Arrange

    # Act
    dataframe_kidney_fixed = ImputeUnivariate.Run(dataframe_kidney, list_name_column=["rbc"], strategy="most_frequent")

    # Assert
    assert 152 == dataframe_kidney["rbc"].isna().sum()
    assert 0 == dataframe_kidney_fixed["rbc"].isna().sum()


@pytest.mark.active
def test_all_most_frequent(dataframe_kidney: pd.DataFrame):
    """Test if the nan in the `rbc` and `pc` column get repaced by "normal"

    :param dataframe_kidney: a dataframe with nans
    :type dataframe_kidney: pd.DataFrame
    """
    # Arrange

    # Act
    dataframe_kidney_fixed = ImputeUnivariate.Run(dataframe_kidney, list_name_column=None, strategy="most_frequent")

    # Assert
    assert 152 == dataframe_kidney["rbc"].isna().sum()
    assert 0 == dataframe_kidney_fixed["rbc"].isna().sum()
    assert 65 == dataframe_kidney["pc"].isna().sum()
    assert 0 == dataframe_kidney_fixed["pc"].isna().sum()
    assert 9 == dataframe_kidney["age"].isna().sum()
    assert 0 == dataframe_kidney_fixed["age"].isna().sum()
    assert pytest.approx(20130.0, 0.0001) == dataframe_kidney["age"].sum()
    assert pytest.approx(20670.0, 0.0001) == dataframe_kidney_fixed["age"].sum()
