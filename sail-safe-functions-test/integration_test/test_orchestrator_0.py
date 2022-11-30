import sys

from sail_safe_functions_orchestrator import preprocessing
from sail_safe_functions_orchestrator.client_rpc_zero import ClientRPCZero
from sail_safe_functions_orchestrator.service_client_dict import ServiceClientDict
from sail_safe_functions_test.test_sail_safe_functions.test_preprocessing.test_convert.convert_to_dataset_tabular_test import (
    test_convert_to_dataset_tabular,
    test_convert_to_dataset_tabular_many_procedure,
    test_convert_to_dataset_tabular_t_test,
)

if __name__ == "__main__":
    # Specific aguments
    hostname = "127.0.0.1"
    port = 5001
    # TODO dataset_longitudinal_r4sep2019_20_1
    dataset_id_longitudinal = "a892ef90-4f6f-11ed-bdc3-0242ac120002"

    # Arrange
    dataset_id_tabular = "a892f738-4f6f-11ed-bdc3-0242ac120002"
    dataset_federation_name = "r4sep2019_csvv1_20_1"
    data_frame_name = "data_frame_0"

    list_dataset_id = [dataset_id_longitudinal]
    client = ClientRPCZero(hostname, port)
    service_client = ServiceClientDict()
    service_client.register_client(dataset_id_longitudinal, client)

    # act
    dataset_longitudinal = preprocessing.read_dataset_fhirv1(service_client, list_dataset_id)
    test_convert_to_dataset_tabular(dataset_longitudinal)
    test_convert_to_dataset_tabular_t_test(dataset_longitudinal)
    test_convert_to_dataset_tabular_many_procedure(dataset_longitudinal)
