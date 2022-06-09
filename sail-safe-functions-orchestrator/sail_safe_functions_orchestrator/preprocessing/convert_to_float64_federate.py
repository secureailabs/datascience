from sail_safe_functions.preprocessing.convert_to_float64 import ConvertFloat64ToTabular, ConvertTabularToFloat64
from sail_safe_functions_orchestrator.dataframe_federated import DataframeFederated


class ConvertTabularToFloat64Federate:
    def run(table_schema: dict, data_frame_source: DataframeFederated) -> DataframeFederated:
        data_frame_target = data_frame_source.create_new()
        for dataset_id in data_frame_source.dict_dataframe:
            data_frame_target.dict_dataframe[dataset_id] = ConvertTabularToFloat64.run(
                table_schema, data_frame_source.dict_dataframe[dataset_id]
            )
        return data_frame_target


class ConvertFloat64ToTabularFederate:
    def run(table_schema: dict, data_frame_source: DataframeFederated) -> DataframeFederated:
        data_frame_target = data_frame_source.create_new()
        for dataset_id in data_frame_source.dict_dataframe:
            data_frame_target.dict_dataframe[dataset_id] = ConvertFloat64ToTabular.run(
                table_schema, data_frame_source.dict_dataframe[dataset_id]
            )
        return data_frame_target
