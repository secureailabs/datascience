from sail_safe_functions_orchestrator.client_rpc_base import ClientRPCBase


class ServiceClient:
    def __init__(self) -> None:
        self.dict_dataset_id_to_client = {}

    ###
    def register_client(self, dataset_id: str, client) -> None:
        self.dict_dataset_id_to_client[dataset_id] = client

    ###
    def get_client(self, dataset_id: str) -> ClientRPCBase:
        if dataset_id not in self.dict_dataset_id_to_client:
            raise ValueError(f"no client for dataset_id: {dataset_id}")
        return self.dict_dataset_id_to_client[dataset_id]
