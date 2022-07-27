from abc import ABC


class SeriesFederated(ABC):
    def __init__(self, name: str = None) -> None:
        self._dict_series = {}
        self.name = name

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
