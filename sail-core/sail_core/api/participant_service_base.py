from abc import abstractmethod
from typing import Any, Dict, List, Type

from sail_core.api.service_base import ServiceBase


class ParticipantServiceBase(ServiceBase):
    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def call(self, node_dataset_id: str, safe_function_class: Type, *argument_list, **argument_dict) -> Any:
        raise NotImplementedError()
