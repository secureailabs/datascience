import pytest
import pandas as pd

from sail_safe_functions.preprocessing.dropna import DropNa


@pytest.mark.active
def test_drop(dataframe_kidney: pd.DataFrame):
    """
    This test our unfederated dropna function

    Args:
        dataframe_kidney (pd.DataFrame): A dataframe with some missing fields
    """
    # Arrange

    # Act
    drop_sail = DropNa.Run(dataframe_kidney, axis=0, how="any", thresh=None, subset=None)
    drop_pandas = pd.DataFrame.dropna(dataframe_kidney, axis=0, how="any", thresh=None, subset=None, inplace=False)

    print(dataframe_kidney.shape)
    print(drop_pandas.shape)
    # Assert
    assert drop_pandas.shape == drop_sail.shape
