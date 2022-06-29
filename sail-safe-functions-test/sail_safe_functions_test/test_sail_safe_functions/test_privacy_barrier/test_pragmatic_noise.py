import pytest
import pandas as pd

from sail_safe_functions.privacy_barrier.pragmatic_noise import PragmaticNoise

@pytest.mark.active
def test_pragmatic_noise(dataframe_kidney_clean: pd.DataFrame, scheme_kidney: dict):
    """
    This tests the pragmatic privacy barrier safe function

    Args:
        dataframe_kidney_clean (pd.DataFrame): A dataframe with no missing fields
    """

    #Arrange

    scheme =  scheme_kidney
    dataset = dataframe_kidney_clean


    #Act
    #noised_data = PragmaticNoise.Run(dataset, scheme, 0.5, 0.5)
