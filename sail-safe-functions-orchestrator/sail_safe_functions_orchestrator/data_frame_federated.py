from abc import ABC


class DataFrameFederated(ABC):
    def __init__(self) -> None:
        self.dict_dataframe = {}

    def create_new(self) -> "DataFrameFederated":
        raise NotImplementedError()
