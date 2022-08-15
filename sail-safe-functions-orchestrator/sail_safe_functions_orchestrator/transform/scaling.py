from abc import abstractmethod

from sail_safe_functions_orchestrator.data_frame_federated import DataFrameFederated
from sail_safe_functions_orchestrator.transform.transform_base import TransformBase


class Scaling(TransformBase):
    def __init__(self) -> None:
        pass

    @abstractmethod
    def fit(self, data_frame: DataFrameFederated):
        raise NotImplementedError()

    def transform(self, data_frame: DataFrameFederated) -> DataFrameFederated:
        raise NotImplementedError()
