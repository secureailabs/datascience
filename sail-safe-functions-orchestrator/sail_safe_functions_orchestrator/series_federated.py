from abc import ABC


class SeriesFederated(ABC):
    def __init__(self) -> None:
        self.dict_series = {}
