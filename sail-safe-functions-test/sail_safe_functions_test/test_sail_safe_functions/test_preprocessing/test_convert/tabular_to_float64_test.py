from typing import Tuple

import pytest
from pandas.util.testing import assert_frame_equal
from sail_safe_functions_orchestrator.preprocessing import convert
from sail_safe_functions_test.helper_sail_safe_functions.data_frame_federated_local import DataFrameFederatedLocal


@pytest.mark.active
def test_convert_and_reverse(tuple_kidney_schema_dataframe: Tuple[dict, DataFrameFederatedLocal]):
    """
    This test or ability to do one-hot and resolution conversion and reverse it relativly acurately (5 decimal places)
    """

    # Arrange
    table_schema = tuple_kidney_schema_dataframe[0]
    data_frame_source = tuple_kidney_schema_dataframe[1]
    dataset_id = list(data_frame_source.dict_dataframe.keys())[0]

    # Act
    date_frame_target = convert.tabular_to_float64(table_schema, data_frame_source)
    date_frame_rebuild = convert.float64_to_tabular(table_schema, date_frame_target)

    # TODO we need to make this nicer at some point
    data_frame_source.dict_dataframe[dataset_id] = data_frame_source.dict_dataframe[dataset_id].drop(["id"], axis=1)
    data_frame_source_raw = data_frame_source.dict_dataframe[dataset_id]
    data_frame_rebuild_raw = date_frame_rebuild.dict_dataframe[dataset_id]

    # Assert
    assert_frame_equal(data_frame_source_raw, data_frame_rebuild_raw)
