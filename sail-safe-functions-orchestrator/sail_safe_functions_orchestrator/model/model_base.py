from abc import ABC, abstractmethod

import pandas
from sail_safe_functions_orchestrator.schema_date_frame import SchemaDataFrame


class ModelBase(ABC):
    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    # TODO make federated
    def fit(data_frame: pandas.DataFrame):
        raise NotImplementedError()

    @abstractmethod
    # TODO make federated
    def predict(data_frame: pandas.DataFrame):
        raise NotImplementedError()
