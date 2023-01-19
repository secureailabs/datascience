from typing import Dict


class DataModelLongitudinal:
    def __init__(self) -> None:
        pass

    def to_dict(self):
        dict = {}
        dict["__type__"] = "DataModelLongitudinal"
        return dict

    @staticmethod
    def from_dict(dict: Dict):
        return DataModelLongitudinal()
