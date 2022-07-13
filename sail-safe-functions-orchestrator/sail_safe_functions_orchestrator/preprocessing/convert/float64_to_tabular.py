from sail_safe_functions.preprocessing.convert.float64_to_tabular_precompute import Float64ToTabularPrecompute
from sail_safe_functions_orchestrator.data_frame_federated import DataFrameFederated
from sail_safe_functions_orchestrator.tools_common import ToolsCommon


def float64_to_tabular(table_schema: dict, data_frame_source: DataFrameFederated) -> DataFrameFederated:
    return Float64ToTabular.run(table_schema, data_frame_source)


class Float64ToTabular:
    def run(table_schema: dict, data_frame_source: DataFrameFederated) -> DataFrameFederated:
        ToolsCommon.check_instance(table_schema, dict)
        ToolsCommon.check_instance(data_frame_source, DataFrameFederated)
        """
        Function used to conver a purely numerical dataframe back to a mixed tabular dataframe.

        :param table_schema: target schema to used for the conversion
        :type table_schema: dict
        :param data_frame_source: dataframe containing only float64 columns
        :type data_frame_source: DataFrameFederated
        :return: new data frame using the schema
        :rtype: DataFrameFederated
        """
        data_frame_target = data_frame_source.create_new()
        for dataset_id in data_frame_source.dict_dataframe:
            data_frame_target.dict_dataframe[dataset_id] = Float64ToTabularPrecompute.run(
                table_schema, data_frame_source.dict_dataframe[dataset_id]
            )
        return data_frame_target
