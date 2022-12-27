from typing import Any, Dict, Type

from sail_core.api.client_rpc_base import ClientRPCBase
from sail_core.api.participant_service_base import ParticipantServiceBase


class ParticipantServiceClientDict(ParticipantServiceBase):
    def __init__(self) -> None:
        self.__dict_client: Dict[str, ClientRPCBase] = {}

    def initialize(self) -> None:
        pass

    def register_client(self, dataset_id: str, client: ClientRPCBase) -> None:
        self.__dict_client[dataset_id] = client

    def get_client(self, dataset_id: str) -> ClientRPCBase:
        if dataset_id not in self.__dict_client:
            raise ValueError(f"no client for dataset_id: {dataset_id}")
        return self.__dict_client[dataset_id]

    def call(self, dataset_id: str, safe_function_class: Type, *argument_list, **argument_dict) -> Any:
        return self.__dict_client[dataset_id].call(safe_function_class, argument_list, argument_dict)
