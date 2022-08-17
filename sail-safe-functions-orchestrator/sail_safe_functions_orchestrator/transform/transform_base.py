from abc import ABC, abstractmethod
from typing import List

from sail_safe_functions_orchestrator.data_frame_federated import DataFrameFederated
from sail_safe_functions_orchestrator.tools_common import check_instance


class TransformBase(ABC):
    def __init__(self) -> None:
        self.list_name_feature = None

    @abstractmethod
    def fit(self, data_frame: DataFrameFederated, list_name_feature: List[str]):
        raise NotImplementedError()

    @abstractmethod
    def transform(self, data_frame: DataFrameFederated) -> DataFrameFederated:
        raise NotImplementedError()

    def fit_transform(self, data_frame: DataFrameFederated, list_name_feature: List[str]) -> DataFrameFederated:
        # check_instance(data_frame, DataFrameFederated)
        self.fit(data_frame, list_name_feature)
        return self.transform(data_frame)
