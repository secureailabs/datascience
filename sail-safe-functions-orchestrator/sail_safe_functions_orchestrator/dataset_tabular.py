from typing import Dict, List

from sail_safe_functions_orchestrator.data_frame import DataFrame
from sail_safe_functions_orchestrator.data_model.data_model_tabular import DataModelTabular
from sail_safe_functions_orchestrator.dataset_base import DatasetBase


class DatasetTabular(DatasetBase):
    def __init__(
        self,
        dataset_federation_id: str,
        dataset_federation_name: str,
        dataset_id: str,
        dataset_name: str,
        list_data_frame: List[DataFrame],
    ) -> None:
        super().__init__(dataset_federation_id, dataset_federation_name, dataset_id, dataset_name)
        # TODO have the data_model validate the dict_table

        self.data_model = DataModelTabular()
        self.dict_data_frame = {}
        for data_frame in list_data_frame:
            self.add_data_frame(data_frame)

    # index section start
    def __delitem__(self, key) -> None:
        raise NotImplementedError()

    def __getitem__(self, key) -> DataFrame:
        # TODO check key typing
        return self.get_data_frame(key)

    def __setitem__(self, key, value):
        raise NotImplementedError()

    # index section end

    # property section start
    @property
    def list_data_frame_name(self) -> List[str]:
        return list(self.dict_data_frame.keys)

    # property section end

    def get_data_frame(self, data_frame_name: str) -> DataFrame:
        if data_frame_name not in self.dict_data_frame:
            raise Exception(f"No such data_frame_model: {data_frame_name}")
        return self.dict_data_frame[data_frame_name]

    def add_data_frame(self, data_frame: DataFrame):
        if data_frame is None:
            raise ValueError(f"data_frame cannot be `None`")
        if data_frame.data_frame_name in self.dict_data_frame:
            raise ValueError(f"Duplicate data_frame: {data_frame.data_frame_name}")
        self.dict_data_frame[data_frame.data_frame_name] = data_frame
        self.data_model.add_data_model_data_frame(data_frame.data_model_data_frame)
