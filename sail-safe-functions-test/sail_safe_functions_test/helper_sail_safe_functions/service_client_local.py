from sail_safe_functions_orchestrator.client_rpc_base import ClientRPCBase
from sail_safe_functions_test.helper_sail_safe_functions.client_rpc_local import ClientRPCLocal


class ServiceClientLocal:
    def __init__(self) -> None:
        self.dict_dataset_id_to_client = {}

    ###
    def register_client(self, dataset_id: str, client) -> None:
        raise NotImplementedError("Cannot register clients here")

    ###
    def get_client(self, dataset_id: str) -> ClientRPCBase:
        return ClientRPCLocal()
