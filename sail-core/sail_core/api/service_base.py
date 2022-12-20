from abc import ABC, abstractmethod
from typing import Dict

from sail_core.implementation_manager import ImplementationMaganger


class ServiceBase(ABC):
    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def initialize(self, implementation_manager: ImplementationMaganger) -> None:
        raise NotImplementedError()
