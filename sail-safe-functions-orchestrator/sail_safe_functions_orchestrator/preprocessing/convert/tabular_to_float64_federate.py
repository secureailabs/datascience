from sail_safe_functions.preprocessing.convert.tabular_to_float64 import TabularToFloat64
from sail_safe_functions_orchestrator.dataframe_federated import DataframeFederated


class TabularToFloat64Federate:
    def run(table_schema: dict, data_frame_source: DataframeFederated) -> DataframeFederated:
        """Function used to convert a mixed tabular datafram containing string columns as well as numerical columns to a purely float64 dataframe for use in machinelearning type operations

        :param table_schema: Schema of the source dataframe
        :type table_schema: dict
        :param data_frame_source: Dataframe to be converted
        :type data_frame_source: DataframeFederated
        :return: Resulting dataframe containg only float64 columns
        :rtype: DataframeFederated
        """
        data_frame_target = data_frame_source.create_new()
        for dataset_id in data_frame_source.dict_dataframe:
            data_frame_target.dict_dataframe[dataset_id] = TabularToFloat64.run(
                table_schema, data_frame_source.dict_dataframe[dataset_id]
            )
        return data_frame_target
