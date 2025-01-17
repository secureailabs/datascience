import pytest
from sail_safe_functions.aggregator import preprocessing
from sail_safe_functions.aggregator.data_frame_federated import DataFrameFederated
from sail_safe_functions.aggregator.service_reference import ServiceReference


@pytest.mark.active
def test_age_exception(data_frame_federated_kidney_hasnan: DataFrameFederated):
    """Test if the strategy parameter gets checked

    :param data_frame_federated_kidney_hasnan: a dataframe with nans
    :type dataframe_kidney: DataFrameFederated
    """
    # Arrange

    # Act
    with pytest.raises(ValueError, match="parameter `strategy` must be either mean, median or most_frequent"):
        preprocessing.impute_univariate(data_frame_federated_kidney_hasnan, list_name_column=["age"], strategy="nope")

    # Assert


@pytest.mark.active
def test_age_mean(data_frame_federated_kidney_hasnan: DataFrameFederated):
    """Test if the 9 nan in the age column get repaced by mean

    :param data_frame_federated_kidney_hasnan: a dataframe with nans
    :type dataframe_kidney: DataFrameFederated
    """
    # Arrange

    # Act
    data_frame_federated_kidney_fixed = preprocessing.impute_univariate(
        data_frame_federated_kidney_hasnan, list_name_column=["age"], strategy="mean"
    )
    reference_data_frame_kidney_fixed = list(data_frame_federated_kidney_fixed.dict_reference_data_frame.values())[0]
    reference_data_frame_kidney = list(data_frame_federated_kidney_hasnan.dict_reference_data_frame.values())[0]
    data_frame_kidney_fixed = ServiceReference.get_instance().reference_to_data_frame(reference_data_frame_kidney_fixed)
    data_frame_kidney = ServiceReference.get_instance().reference_to_data_frame(reference_data_frame_kidney)
    # Assert
    assert 9 == data_frame_kidney["age"].isna().sum()
    assert 0 == data_frame_kidney_fixed["age"].isna().sum()
    assert pytest.approx(20130.0, 0.0001) == data_frame_kidney["age"].sum()
    assert pytest.approx(20593.35038363171, 0.0001) == data_frame_kidney_fixed["age"].sum()


@pytest.mark.active
def test_age_median(data_frame_federated_kidney_hasnan: DataFrameFederated):
    """Test if the 9 nan in the age column get repaced by median

    :param data_frame_federated_kidney: a dataframe with nans
    :type dataframe_kidney: DataFrameFederated
    """
    # Arrange

    # Act
    data_frame_federated_kidney_fixed = preprocessing.impute_univariate(
        data_frame_federated_kidney_hasnan, list_name_column=["age"], strategy="median"
    )
    reference_data_frame_kidney_fixed = list(data_frame_federated_kidney_fixed.dict_reference_data_frame.values())[0]
    reference_data_frame_kidney = list(data_frame_federated_kidney_hasnan.dict_reference_data_frame.values())[0]
    data_frame_kidney_fixed = ServiceReference.get_instance().reference_to_data_frame(reference_data_frame_kidney_fixed)
    data_frame_kidney = ServiceReference.get_instance().reference_to_data_frame(reference_data_frame_kidney)

    # Assert
    assert 9 == data_frame_kidney["age"].isna().sum()
    assert 0 == data_frame_kidney_fixed["age"].isna().sum()
    assert pytest.approx(20130.0, 0.0001) == data_frame_kidney["age"].sum()
    assert pytest.approx(20625.0, 0.0001) == data_frame_kidney_fixed["age"].sum()


@pytest.mark.active
def test_age_most_frequent(data_frame_federated_kidney_hasnan: DataFrameFederated):
    """Test if the string insertion gets rejected

    :param data_frame_federated_kidney_hasnan: a dataframe with nans
    :type dataframe_kidney: DataFrameFederated
    """
    # Arrange

    # Act
    data_frame_federated_kidney_fixed = preprocessing.impute_univariate(
        data_frame_federated_kidney_hasnan, list_name_column=["age"], strategy="most_frequent"
    )
    reference_data_frame_kidney_fixed = list(data_frame_federated_kidney_fixed.dict_reference_data_frame.values())[0]
    reference_data_frame_kidney = list(data_frame_federated_kidney_hasnan.dict_reference_data_frame.values())[0]
    data_frame_kidney_fixed = ServiceReference.get_instance().reference_to_data_frame(reference_data_frame_kidney_fixed)
    data_frame_kidney = ServiceReference.get_instance().reference_to_data_frame(reference_data_frame_kidney)

    # Assert
    assert 9 == data_frame_kidney["age"].isna().sum()
    assert 0 == data_frame_kidney_fixed["age"].isna().sum()
    assert pytest.approx(20130.0, 0.0001) == data_frame_kidney["age"].sum()
    assert pytest.approx(20670.0, 0.0001) == data_frame_kidney_fixed["age"].sum()


@pytest.mark.active
def test_rbc_exception(data_frame_federated_kidney_hasnan: DataFrameFederated):
    """Test if the 152 nan in the `rbc` column raise an exception when mean is used

    :param data_frame_federated_kidney_hasnan: a dataframe with nans
    :type dataframe_kidney: DataFrameFederated
    """
    # Arrange

    # Act
    with pytest.raises(
        ValueError,
        match="`mean`, `median` strategies cannot not operate on series with series_name rbc which is of string type",
    ):
        data_frame_federated_kidney_fixed = preprocessing.impute_univariate(
            data_frame_federated_kidney_hasnan, list_name_column=["rbc"], strategy="mean"
        )

    # Assert


@pytest.mark.active
def test_rbc_most_frequent(data_frame_federated_kidney_hasnan: DataFrameFederated):
    """Test if the 152 nan in the `rbc` column get repaced by "most_frequent"

    :param data_frame_federated_kidney: a dataframe with nans
    :type dataframe_kidney: DataFrameFederated
    """
    # Arrange

    # Act
    data_frame_federated_kidney_fixed = preprocessing.impute_univariate(
        data_frame_federated_kidney_hasnan, list_name_column=["rbc"], strategy="most_frequent"
    )

    reference_data_frame_kidney_fixed = list(data_frame_federated_kidney_fixed.dict_reference_data_frame.values())[0]
    reference_data_frame_kidney = list(data_frame_federated_kidney_hasnan.dict_reference_data_frame.values())[0]
    data_frame_kidney_fixed = ServiceReference.get_instance().reference_to_data_frame(reference_data_frame_kidney_fixed)
    data_frame_kidney = ServiceReference.get_instance().reference_to_data_frame(reference_data_frame_kidney)
    # Assert
    assert 152 == data_frame_kidney["rbc"].isna().sum()
    assert 0 == data_frame_kidney_fixed["rbc"].isna().sum()


@pytest.mark.active
def test_all_most_frequent(data_frame_federated_kidney_hasnan: DataFrameFederated):
    """Test if the nan in the `rbc` and `pc` column get repaced by "normal"

    :param data_frame_federated_kidney: a dataframe with nans
    :type dataframe_kidney: DataFrameFederated
    """
    # Arrange

    # Act
    data_frame_federated_kidney_fixed = preprocessing.impute_univariate(
        data_frame_federated_kidney_hasnan, list_name_column=None, strategy="most_frequent"
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
    assert 9 == data_frame_kidney["age"].isna().sum()
    assert 0 == data_frame_kidney_fixed["age"].isna().sum()
    assert pytest.approx(20130.0, 0.0001) == data_frame_kidney["age"].sum()
    assert pytest.approx(20670.0, 0.0001) == data_frame_kidney_fixed["age"].sum()
