from sail_safe_functions.preprocessing.convert.tabular_to_float64_precompute import (
    TabularToFloat64Precompute,
)
from sail_safe_functions_orchestrator.data_frame_federated import DataFrameFederated
from sail_safe_functions_orchestrator.tools_common import check_instance


def tabular_to_float64(
    table_schema: dict, data_frame_source: DataFrameFederated
) -> DataFrameFederated:
    return TabularToFloat64.run(table_schema, data_frame_source)


class TabularToFloat64:
    def run(
        table_schema: dict, data_frame_source: DataFrameFederated
    ) -> DataFrameFederated:
        check_instance(table_schema, dict)
        check_instance(data_frame_source, DataFrameFederated)
        """
        Function used to convert a mixed tabular datafram containing string columns as well as numerical columns to a purely float64 dataframe for use in machinelearning type operations

        :param table_schema: Schema of the source dataframe
        :type table_schema: dict
        :param data_frame_source: Dataframe to be converted
        :type data_frame_source: DataFrameFederated
        :return: Resulting dataframe containg only float64 columns
        :rtype: DataFrameFederated
        """
        data_frame_target = data_frame_source.create_new()
        for dataset_id in data_frame_source.dict_dataframe:
            data_frame_target.dict_dataframe[
                dataset_id
            ] = TabularToFloat64Precompute.Run(
                table_schema, data_frame_source.dict_dataframe[dataset_id]
            )
        return data_frame_target
