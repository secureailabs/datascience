from sail_safe_functions.aggregator.client_rpc_base import ClientRPCBase
from sail_safe_functions.aggregator.service_client_base import ServiceClientBase


class ServiceClientDict(ServiceClientBase):
    def __init__(self) -> None:
        self._dict_dataset_id_to_client = {}

    def register_client(self, dataset_id: str, client: ClientRPCBase) -> None:
        self._dict_dataset_id_to_client[dataset_id] = client

    def get_client(self, dataset_id: str) -> ClientRPCBase:
        if dataset_id not in self._dict_dataset_id_to_client:
            raise ValueError(f"no client for dataset_id: {dataset_id}")
        return self._dict_dataset_id_to_client[dataset_id]
