import pandas
import pytest
from sail_safe_functions_orchestrator import preprocessing
from sail_safe_functions_orchestrator.data_frame_federated import DataFrameFederated
from sail_safe_functions_orchestrator.service_reference import ServiceReference


@pytest.mark.active
def test_drop_series_with_missing(data_frame_federated_kidney_hasnan: DataFrameFederated):
    """
    This tests our federated drop_series_with_missing function

    Args:
        federated_dataframe_kidney (DataFrameFederated): A dataframe with some missing fields
    """
    # Arrange

    # Act
    data_frame_federated_kidney_fixed = preprocessing.drop_missing(
        data_frame_federated_kidney_hasnan, axis=1, how="any", thresh=None, subset=None
    )

    reference_data_frame_kidney_fixed = list(data_frame_federated_kidney_fixed.dict_reference_data_frame.values())[0]
    reference_data_frame_kidney = list(data_frame_federated_kidney_hasnan.dict_reference_data_frame.values())[0]
    data_frame_kidney_fixed = ServiceReference.get_instance().reference_to_data_frame(reference_data_frame_kidney_fixed)
    data_frame_kidney = ServiceReference.get_instance().reference_to_data_frame(reference_data_frame_kidney)
    data_frame_kidney_direct = pandas.DataFrame.dropna(
        data_frame_kidney, axis=1, how="any", thresh=None, subset=None, inplace=False
    )

    # Assert
    assert data_frame_kidney_direct.shape == data_frame_kidney_fixed.shape


@pytest.mark.active
def test_drop_rows_with_missing(data_frame_federated_kidney_hasnan: DataFrameFederated):
    """
    This tests our federated drop_series_with_missing function

    Args:
        federated_dataframe_kidney (DataFrameFederated): A dataframe with some missing fields
    """
    # Arrange

    # Act
    data_frame_federated_kidney_fixed = preprocessing.drop_missing(
        data_frame_federated_kidney_hasnan, axis=0, how="any", thresh=None, subset=None
    )

    reference_data_frame_kidney_fixed = list(data_frame_federated_kidney_fixed.dict_reference_data_frame.values())[0]
    reference_data_frame_kidney = list(data_frame_federated_kidney_hasnan.dict_reference_data_frame.values())[0]
    data_frame_kidney_fixed = ServiceReference.get_instance().reference_to_data_frame(reference_data_frame_kidney_fixed)
    data_frame_kidney = ServiceReference.get_instance().reference_to_data_frame(reference_data_frame_kidney)
    data_frame_kidney_direct = pandas.DataFrame.dropna(
        data_frame_kidney, axis=0, how="any", thresh=None, subset=None, inplace=False
    )

    # Assert
    assert data_frame_kidney_direct.shape == data_frame_kidney_fixed.shape
