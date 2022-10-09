import pandas as pd
import pytest
from sail_safe_functions_orchestrator.privacy import add_noise_to_dataset_client

# @pytest.mark.active
# def test_pragmatic_noise(
#     connect_to_one_VM,
#     dataframe_kidney_clean_remote,
#     scheme_kidney,
# ):
#     """
#     This tests the pragmatic privacy barrier safe function
#     Args:
#         dataframe_kidney_clean (pd.DataFrame): A dataframe with no missing fields
#         scheme_kidney (pd.DataFrame): A scheme for the kidney dataframe
#     """

#     # Arrange

#     scheme = scheme_kidney
#     dataset = dataframe_kidney_clean_remote
#     client = connect_to_one_VM

#     # Act
#     noised_data = add_noise_to_dataset_client(client, dataset, scheme, 0.5, 0.5)

#     # Assert
#     assert type(noised_data) is pd.DataFrame

#     # TODO add assert to measure privacy loss between original data and new (KL Divergence Needed)
