from sail_safe_functions.aggregator.data_frame_federated import DataFrameFederated
from sail_safe_functions.aggregator.tools_common import check_instance
from sail_safe_functions.participant.preprocessing.convert.tabular_to_float64_precompute import (
    TabularToFloat64Precompute,
)
from sail_safe_functions.safe_function_base import SafeFunctionBase


def tabular_to_float64(
    data_frame_source: DataFrameFederated,
) -> DataFrameFederated:
    """
    Function used to convert a mixed tabular datafram containing string columns as well as numerical columns to a purely float64 dataframe for use in machinelearning type operations

        :param data_frame_source: Dataframe to be converted
        :type data_frame_source: DataFrameFederated
        :return: Resulting dataframe containg only float64 columns
        :rtype: DataFrameFederated

    Example:

        from sail_safe_functions.aggregator.preprocessing import convert
        imports pandas as pd

        #this is example datset you can use any csv file
        tuple_kidney_schema_dataframe = pd.read_csv("./tuple_kidney_schema_dataframe")
        table_schema = tuple_kidney_schema_dataframe[0]
        data_frame_source = tuple_kidney_schema_dataframe[1]
        dataset_id = list(data_frame_source.dict_dataframe.keys())[0]

        date_frame_target = convert.tabular_to_float64(table_schema, data_frame_source)

    """
    return TabularToFloat64.run(data_frame_source)


class TabularToFloat64(SafeFunctionBase):
    @staticmethod
    def run(
        data_frame_source: DataFrameFederated,
    ) -> DataFrameFederated:
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

        list_reference = data_frame_source.map_function(TabularToFloat64Precompute)
        return DataFrameFederated(list_reference, list_reference[0].data_model_data_frame)
