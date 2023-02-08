from abc import ABC
from typing import List


class Estimator(ABC):
    def __init__(self, estimator_name: str, list_estimate_name: List[str]) -> None:
        self.__estimator_name = estimator_name
        self.__list_estimate_name = list_estimate_name

    def get_estimate_index(self, estimate_name_requested: str) -> int:
        for i, estimate_name in enumerate(self.__list_estimate_name):
            if estimate_name == estimate_name_requested:
                return i
        raise Exception(f"no such estimate in estimator {estimate_name_requested}")

    @property
    def estimator_name(self) -> str:
        return self.__estimator_name

    @property
    def list_estimate_name(self) -> List[str]:
        return self.__list_estimate_name.copy()
