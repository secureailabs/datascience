import pandas as pd
import pytest
from sail_safe_functions.privacy_barrier.pragmatic_noise import PragmaticNoise
from sail_safe_functions_orchestrator.data_frame_federated import DataFrameFederated
from sail_safe_functions_orchestrator.service_reference import ServiceReference


@pytest.mark.active
def test_pragmatic_noise(data_frame_federated_kidney: DataFrameFederated):
    """
    This tests the pragmatic privacy barrier safe function

    Args:
        dataframe_kidney_clean (pd.DataFrame): A dataframe with no missing fields
        scheme_kidney (pd.DataFrame): A scheme for the kidney dataframe

    """

    # Arrang
    reference_data_frame_source = list(data_frame_federated_kidney.dict_reference_data_frame.values())[0]
    data_frame_source = ServiceReference.get_instance().reference_to_data_frame(reference_data_frame_source)
    data_model_data_frame = data_frame_federated_kidney.data_model_data_frame
    # Act
    pragmatic_noise = PragmaticNoise()
    noised_data = pragmatic_noise.run(data_frame_source, data_model_data_frame, 0.5, 0.5)

    # Assert
    assert type(noised_data) is pd.DataFrame

    # TODO add assert to measure privacy loss between original data and new (KL Divergence Needed)
