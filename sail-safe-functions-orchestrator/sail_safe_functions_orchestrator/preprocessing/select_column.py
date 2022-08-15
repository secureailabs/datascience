from typing import Any, List

from sail_safe_functions.preprocessing.select_column_precompute import SelectColumnPrecompute
from sail_safe_functions_orchestrator.data_frame_federated import DataFrameFederated
from sail_safe_functions_orchestrator.tools_common import check_instance


def select_column(data_frame_source: DataFrameFederated, list_name_column: List[str]) -> DataFrameFederated:
    return SelectColumn.run(data_frame_source, list_name_column)


class SelectColumn:
    """
    Select columns
    """

    def run(
        data_frame_source: DataFrameFederated,
        list_name_column: List[str],
    ) -> DataFrameFederated:
        check_instance(data_frame_source, DataFrameFederated)
        check_instance(list_name_column, List)
        data_frame_target = data_frame_source.create_new()
        for dataset_id in data_frame_source.dict_dataframe:
            data_frame_target.dict_dataframe[dataset_id] = SelectColumnPrecompute.run(
                data_frame_source.dict_dataframe[dataset_id],
                list_name_column,
            )
        return data_frame_target
