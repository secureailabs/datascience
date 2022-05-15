from abc import ABC


class SeriesFederated(ABC):
    def __init__(self) -> None:
        self._dict_series = {}
        self.name = None
        self.size = 0

    def items(self):
        return self._dict_series.items()
