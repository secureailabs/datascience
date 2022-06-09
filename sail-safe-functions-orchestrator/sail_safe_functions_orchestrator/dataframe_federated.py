from abc import ABC


class DataframeFederated(ABC):
    def __init__(self) -> None:
        self.dict_dataframe = {}

    def create_new(self) -> "DataframeFederated":
        raise NotImplementedError()
