from abc import ABC, abstractmethod

from sail_safe_functions.aggregator.client_rpc_base import ClientRPCBase


class ServiceClientBase(ABC):
    @abstractmethod
    def get_client(self, dataset_id: str) -> ClientRPCBase:
        raise NotImplementedError()
