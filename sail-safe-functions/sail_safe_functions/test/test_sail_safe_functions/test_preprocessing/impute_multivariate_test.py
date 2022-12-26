import pytest
from sail_safe_functions.aggregator import preprocessing
from sail_safe_functions.aggregator.data_frame_federated import DataFrameFederated
from sail_safe_functions.aggregator.service_reference import ServiceReference


@pytest.mark.active
def test_exception(data_frame_federated_kidney: DataFrameFederated):
    """Test if the imputation_order parameter gets checked

    :param data_frame_federated_kidney: a dataframe with nans
    :type dataframe_kidney: DataFrameFederated
    """
    # Arrange

    # Act
    with pytest.raises(
        ValueError,
        match="`imputation_order` must be either in {`ascending`, `descending`}",
    ):
        preprocessing.impute_multivariate(
            data_frame_federated_kidney, list_name_column=["age"], imputation_order="nope"
        )

    # Assert


@pytest.mark.active
def test_age(data_frame_federated_kidney_hasnan: DataFrameFederated):
    """Test if the 9 nan in the age column get repaced by multivariate estimation

    :param data_frame_federated_kidney_hasnan: a dataframe with nans
    :type dataframe_kidney: DataFrameFederated
    """
    # Arrange

    # Act
    data_frame_federated_kidney_fixed = preprocessing.impute_multivariate(
        data_frame_federated_kidney_hasnan,
        list_name_column=["age"],
        imputation_order="ascending",
        max_iter=20,
    )

    reference_data_frame_kidney_fixed = list(data_frame_federated_kidney_fixed.dict_reference_data_frame.values())[0]
    reference_data_frame_kidney = list(data_frame_federated_kidney_hasnan.dict_reference_data_frame.values())[0]

    data_frame_kidney_fixed = ServiceReference.get_instance().reference_to_data_frame(reference_data_frame_kidney_fixed)
    data_frame_kidney = ServiceReference.get_instance().reference_to_data_frame(reference_data_frame_kidney)

    # Assert
    assert 9 == data_frame_kidney["age"].isna().sum()
    assert 0 == data_frame_kidney_fixed["age"].isna().sum()
    assert pytest.approx(20130.0, 0.0001) == data_frame_kidney["age"].sum()
    assert pytest.approx(20604.530413505294, 0.0001) == data_frame_kidney_fixed["age"].sum()


@pytest.mark.active
def test_rbc(data_frame_federated_kidney_hasnan: DataFrameFederated):
    """Test if the 152 nan in the `rbc` column get repaced by "most_frequent"

    :param data_frame_federated_kidney_hasnan: a dataframe with nans
    :type dataframe_kidney: DataFrameFederated
    """
    # Arrange

    # Act
    data_frame_federated_kidney_fixed = preprocessing.impute_multivariate(
        data_frame_federated_kidney_hasnan,
        list_name_column=["rbc"],
        imputation_order="ascending",
        max_iter=20,
    )

    reference_data_frame_kidney_fixed = list(data_frame_federated_kidney_fixed.dict_reference_data_frame.values())[0]
    reference_data_frame_kidney = list(data_frame_federated_kidney_hasnan.dict_reference_data_frame.values())[0]
    data_frame_kidney_fixed = ServiceReference.get_instance().reference_to_data_frame(reference_data_frame_kidney_fixed)
    data_frame_kidney = ServiceReference.get_instance().reference_to_data_frame(reference_data_frame_kidney)

    # Assert
    assert 152 == data_frame_kidney["rbc"].isna().sum()
    assert 0 == data_frame_kidney_fixed["rbc"].isna().sum()


@pytest.mark.active
def test_all(data_frame_federated_kidney_hasnan: DataFrameFederated):
    """Test if all the nan in the dataframe get repaced

    :param data_frame_federated_kidney: a dataframe with nans
    :type dataframe_kidney: DataFrameFederated
    """
    # Arrange

    # Act
    data_frame_federated_kidney_fixed = preprocessing.impute_multivariate(
        data_frame_federated_kidney_hasnan,
        list_name_column=None,
        imputation_order="ascending",
        max_iter=20,
    )

    reference_data_frame_kidney_fixed = list(data_frame_federated_kidney_fixed.dict_reference_data_frame.values())[0]
    reference_data_frame_kidney = list(data_frame_federated_kidney_hasnan.dict_reference_data_frame.values())[0]
    data_frame_kidney_fixed = ServiceReference.get_instance().reference_to_data_frame(reference_data_frame_kidney_fixed)
    data_frame_kidney = ServiceReference.get_instance().reference_to_data_frame(reference_data_frame_kidney)

    # Assert
    assert 152 == data_frame_kidney["rbc"].isna().sum()
    assert 65 == data_frame_kidney["pc"].isna().sum()
    assert 9 == data_frame_kidney["age"].isna().sum()

    for name_column in data_frame_kidney_fixed.columns:
        assert 0 == data_frame_kidney_fixed[name_column].isna().sum()

    assert pytest.approx(20130.0, 0.0001) == data_frame_kidney["age"].sum()
    assert pytest.approx(20604.530413505294, 0.0001) == data_frame_kidney_fixed["age"].sum()
