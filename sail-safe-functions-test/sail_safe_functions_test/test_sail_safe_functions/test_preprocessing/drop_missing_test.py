import imp

import pandas
import pytest
from sail_safe_functions_orchestrator import preprocessing
from sail_safe_functions_orchestrator.data_frame_federated import DataFrameFederated


@pytest.mark.active
def test_drop(data_frame_federated_kidney: DataFrameFederated):
    """
    This tests our federated drop_missing function

    Args:
        federated_dataframe_kidney (DataFrameFederated): A dataframe with some missing fields
    """
    # Arrange
    data_frame_kidney = list(data_frame_federated_kidney.dict_dataframe.values())[0]

    # Act
    drop_sail = preprocessing.drop_missing(data_frame_federated_kidney, axis=0, how="any", thresh=None, subset=None)
    drop_pandas = pandas.DataFrame.dropna(data_frame_kidney, axis=0, how="any", thresh=None, subset=None, inplace=False)

    # Assert
    assert drop_pandas.shape == list(drop_sail.dict_dataframe.values())[0].shape
