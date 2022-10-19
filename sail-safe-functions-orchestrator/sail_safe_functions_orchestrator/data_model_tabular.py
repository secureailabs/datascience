from typing import Dict

from sail_safe_functions_orchestrator.data_model_feature import DataModelFeature
from sail_safe_functions_orchestrator.data_model_table import DataModelTable


class DataModelTabular:
    def __init__(self) -> None:
        self.dict_data_model_table = {}  # This could be an ordered dict but they do not map to json by default

    def get_data_model_table(self, table_id: str) -> DataModelTable:
        if table_id not in self.dict_data_model_table:
            raise Exception(f"No such table: {table_id}")
        return self.dict_data_model_table[table_id]

    def add_data_model_table(self, data_model_table: DataModelTable) -> None:
        if data_model_table.table_name in self.dict_data_model_table:
            raise Exception(f"Duplicate table_name: {data_model_table.table_name}")
        self.dict_data_model_table[data_model_table.table_id] = data_model_table

    def to_json(self) -> Dict:
        dict_json = {}
        dict_json["dict_data_model_table"] = {}
        for table_id, data_model_table in self.dict_data_model_table.items():
            dict_json["dict_data_model_table"][table_id] = data_model_table.t
        return dict_json

    @staticmethod
    def from_json(dict_json: Dict) -> "DataModelTabular":
        data_model_tabular = DataModelTabular()
        for table_id, data_model_table in dict_json["dict_data_model_table"].items():
            data_model_tabular.dict_data_model_table[table_id] = DataModelTable.from_json(data_model_table)
        return data_model_tabular
