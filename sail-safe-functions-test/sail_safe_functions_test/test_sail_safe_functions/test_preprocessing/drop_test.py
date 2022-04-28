import pytest
import pandas as pd

from sail_safe_functions.preprocessing.drop import Drop


@pytest.mark.active
def test_drop(dataframe_kidney: pd.DataFrame):
    """
    This test our unfederated drop function

    Args:
        dataframe_kidney (pd.DataFrame): A dataframe with some missing fields
    """
    # Arrange

    # Act

    drop_sail = Drop.Run(dataframe_kidney, labels=[0, 1], axis=0, index=None, columns=None, level=None, errors="raise")
    drop_pandas = pd.DataFrame.drop(
        dataframe_kidney, labels=[0, 1], axis=0, index=None, columns=None, level=None, inplace=False, errors="raise"
    )

    # Assert
    assert drop_pandas.shape == drop_sail.shape
