import pytest
from sail_safe_functions.aggregator import preprocessing
from sail_safe_functions.aggregator.data_frame_federated import DataFrameFederated
from sail_safe_functions.aggregator.service_reference import ServiceReference


@pytest.mark.broken
def test_convert_and_reverse(data_frame_federated_kidney: DataFrameFederated):
    """
    This test or ability to do one-hot and resolution conversion and reverse it relativly acurately (5 decimal places)
    """

    # Act
    data_frame_federated_source = data_frame_federated_kidney
    data_frame_federated_result = preprocessing.tabular_to_float64(data_frame_federated_source)
    date_frame_federated_rebuild = preprocessing.float64_to_tabular(
        data_frame_federated_result, data_frame_federated_source.data_model_data_frame
    )

    reference_data_frame_source = list(data_frame_federated_source.dict_reference_data_frame.values())[0]
    reference_data_frame_rebuild = list(date_frame_federated_rebuild.dict_reference_data_frame.values())[0]
    data_frame_source = ServiceReference.get_instance().reference_to_data_frame(reference_data_frame_source)
    data_frame_rebuild = ServiceReference.get_instance().reference_to_data_frame(reference_data_frame_rebuild)

    # Assert
    # TODO this test has been playing up, the problem with is is the equals function at the very
    #  bottom i think it should be overloaded and we might also need an is_close
    assert data_frame_source.equals(data_frame_rebuild)
