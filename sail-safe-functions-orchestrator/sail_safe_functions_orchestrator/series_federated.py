from abc import ABC
from typing import List, Tuple


class SeriesFederated(ABC):
    def __init__(self, name: str = None) -> None:
        self._dict_series = {}
        self.name = name
        self._dtype = None

    @property
    def dtype(self):
        return self._dtype

    @property
    def dict_series(self):
        return self._dict_series

    @property
    def size(self):
        size = 0
        for series in self._dict_series.values():
            size += series.size
        return size

    def items(self):
        return self._dict_series.items()

    def create_new(self) -> "SeriesFederated":
        raise NotImplementedError()
