from sail_safe_functions.preprocessing.convert.float64_to_tabular import ConvertFloat64ToTabular
from sail_safe_functions_orchestrator.dataframe_federated import DataframeFederated


class Float64ToTabularFederate:
    def run(table_schema: dict, data_frame_source: DataframeFederated) -> DataframeFederated:
        """
        Function used to conver a purely numerical dataframe back to a mixed tabular dataframe.

        :param table_schema: target schema to used for the conversion
        :type table_schema: dict
        :param data_frame_source: dataframe containing only float64 columns
        :type data_frame_source: DataframeFederated
        :return: new data frame using the schema
        :rtype: DataframeFederated
        """
        data_frame_target = data_frame_source.create_new()
        for dataset_id in data_frame_source.dict_dataframe:
            data_frame_target.dict_dataframe[dataset_id] = ConvertFloat64ToTabular.run(
                table_schema, data_frame_source.dict_dataframe[dataset_id]
            )
        return data_frame_target
