import pandas as pd
import pytest
from sail_safe_functions_orchestrator import preprocessing
from sail_safe_functions_orchestrator.data_frame_federated import DataFrameFederated


@pytest.mark.active
def test_drop(data_frame_federated_kidney: DataFrameFederated):
    """
    This tests our federated drop function

    Args:
        federated_dataframe_kidney (DataFrameFederated): A dataframe with some missing fields
    """
    # Arrange
    data_frame_kidney = list(data_frame_federated_kidney.dict_dataframe.values())[0]

    # Act
    drop_sail = preprocessing.drop(
        data_frame_federated_kidney,
        labels=[0, 1],
        axis=0,
        index=None,
        columns=None,
        level=None,
        errors="raise",
    )
    drop_sail = list(drop_sail.dict_dataframe.values())[0]
    drop_pandas = pd.DataFrame.drop(
        data_frame_kidney, labels=[0, 1], axis=0, index=None, columns=None, level=None, inplace=False, errors="raise"
    )

    # Assert
    assert drop_pandas.shape == drop_sail.shape
