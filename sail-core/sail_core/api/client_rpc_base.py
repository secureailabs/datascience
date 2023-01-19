from abc import abstractmethod
from typing import Type


class ClientRPCBase:
    @abstractmethod
    def call(self, safe_function_class: Type, *arguments_list, **arguments_dict):
        raise NotImplementedError()
