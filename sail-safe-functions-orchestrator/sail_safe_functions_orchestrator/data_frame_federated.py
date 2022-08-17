from abc import ABC, abstractmethod
from typing import List, Tuple

from sail_safe_functions_orchestrator.series_federated import SeriesFederated


class DataFrameFederated(ABC):
    def __init__(self) -> None:
        self.dict_dataframe = {}

    @property
    def shape(self) -> Tuple[float, float]:
        return (self.size, len(self.list_name_feature))

    @property
    def list_name_feature(self) -> List[str]:
        return self.columns

    @property
    @abstractmethod
    def size(self) -> int:
        raise NotImplementedError()

    @property
    @abstractmethod
    def columns(self) -> List[str]:
        raise NotImplementedError()

    @abstractmethod
    def create_new(self) -> "DataFrameFederated":
        raise NotImplementedError()

    # index section
    @abstractmethod
    def __delitem__(self, key) -> None:
        raise NotImplementedError()

    @abstractmethod
    def __getitem__(self, key) -> SeriesFederated:
        raise NotImplementedError()

    @abstractmethod
    def __setitem__(self, key, value):
        raise NotImplementedError()
