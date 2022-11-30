from abc import ABC, abstractmethod

from sail_safe_functions_orchestrator.client_rpc_base import ClientRPCBase


class ServiceClientBase(ABC):
    @abstractmethod
    def get_client(self, dataset_id: str) -> ClientRPCBase:
        raise NotImplementedError()
