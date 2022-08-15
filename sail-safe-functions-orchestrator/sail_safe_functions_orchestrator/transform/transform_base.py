from abc import ABC, abstractmethod

from sail_safe_functions_orchestrator.data_frame_federated import DataFrameFederated


class TransformBase(ABC):
    def __init__(self) -> None:
        pass

    @abstractmethod
    def fit(self, data_frame: DataFrameFederated):
        raise NotImplementedError()

    @abstractmethod
    def transform(self, data_frame: DataFrameFederated) -> DataFrameFederated:
        raise NotImplementedError()

    def fit_transform(self, data_frame: DataFrameFederated) -> DataFrameFederated:
        self.fit(data_frame)
        return self.transform(data_frame)
