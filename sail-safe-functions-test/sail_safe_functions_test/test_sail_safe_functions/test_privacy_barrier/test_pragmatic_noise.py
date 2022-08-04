import pandas as pd
import pytest
from sail_safe_functions.privacy_barrier.pragmatic_noise_precompute import PragmaticNoisePrecompute


@pytest.mark.active
def test_pragmatic_noise(dataframe_kidney_clean: pd.DataFrame, scheme_kidney: dict):
    """
    This tests the pragmatic privacy barrier safe function

    Args:
        dataframe_kidney_clean (pd.DataFrame): A dataframe with no missing fields
        scheme_kidney (pd.DataFrame): A scheme for the kidney dataframe

    """

    # Arrange

    scheme = scheme_kidney
    dataset = dataframe_kidney_clean

    # Act
    noised_data = PragmaticNoisePrecompute.run(dataset, scheme, 0.5, 0.5)

    # Assert
    assert type(noised_data) is pd.DataFrame

    # TODO add assert to measure privacy loss between original data and new (KL Divergence Needed)
