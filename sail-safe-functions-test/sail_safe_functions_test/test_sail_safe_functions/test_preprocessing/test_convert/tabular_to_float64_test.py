import pytest
from sail_safe_functions_orchestrator.data_frame_federated import DataFrameFederated
from sail_safe_functions_orchestrator.preprocessing import convert
from sail_safe_functions_orchestrator.service_reference import ServiceReference


@pytest.mark.active
def test_convert_and_reverse(data_frame_federated_kidney: DataFrameFederated):
    """
    This test or ability to do one-hot and resolution conversion and reverse it relativly acurately (5 decimal places)
    """

    # Act
    data_frame_federated_source = data_frame_federated_kidney
    data_frame_federated_result = convert.tabular_to_float64(data_frame_federated_source)
    date_frame_federated_rebuild = convert.float64_to_tabular(
        data_frame_federated_result, data_frame_federated_source.data_model_data_frame
    )

    reference_data_frame_source = list(data_frame_federated_source.dict_reference_data_frame.values())[0]
    reference_data_frame_rebuild = list(date_frame_federated_rebuild.dict_reference_data_frame.values())[0]
    data_frame_source = ServiceReference.get_instance().reference_to_data_frame(reference_data_frame_source)
    data_frame_rebuild = ServiceReference.get_instance().reference_to_data_frame(reference_data_frame_rebuild)

    # Assert
    assert data_frame_source.equals(data_frame_rebuild)
