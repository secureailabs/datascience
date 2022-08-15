from abc import ABC, abstractmethod
from typing import List


class DataFrameFederated(ABC):
    def __init__(self) -> None:
        self.dict_dataframe = {}

    @property
    @abstractmethod
    def columns(self) -> List[str]:
        raise NotImplementedError()

    def create_new(self) -> "DataFrameFederated":
        raise NotImplementedError()
