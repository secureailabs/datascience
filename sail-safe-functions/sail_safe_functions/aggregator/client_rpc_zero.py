from typing import Type

from sail_core.api.client_rpc_base import ClientRPCBase
from sail_core.tools_common import check_instance
from sail_safe_functions.aggregator.data_model.data_model_data_frame import DataModelDataFrame
from sail_safe_functions.aggregator.data_model.data_model_longitudinal import DataModelLongitudinal
from sail_safe_functions.aggregator.data_model.data_model_series import DataModelSeries
from sail_safe_functions.aggregator.data_model.data_model_tabular import DataModelTabular
from sail_safe_functions.aggregator.reference_data_frame import ReferenceDataFrame
from sail_safe_functions.aggregator.reference_dataset_longitudinal import ReferenceDatasetLongitudinal
from sail_safe_functions.aggregator.reference_dataset_tabular import ReferenceDatasetTabular
from sail_safe_functions.aggregator.reference_series import ReferenceSeries
from zero import ZeroClient

# TODO move this somewhere


class ClientRPCZero(ClientRPCBase):
    def __init__(self, hostname: str, port: int) -> None:
        super().__init__()
        self._zero_client = ZeroClient(hostname, port)

        self._zero_client._serializer_table["ReferenceDatasetLongitudinal"] = ReferenceDatasetLongitudinal
        self._zero_client._serializer_table["ReferenceDatasetTabular"] = ReferenceDatasetTabular
        self._zero_client._serializer_table["ReferenceDataFrame"] = ReferenceDataFrame
        self._zero_client._serializer_table["ReferenceSeries"] = ReferenceSeries
        self._zero_client._serializer_table["DataModelTabular"] = DataModelTabular
        self._zero_client._serializer_table["DataModelLongitudinal"] = DataModelLongitudinal
        self._zero_client._serializer_table["DataModelDataFrame"] = DataModelDataFrame
        self._zero_client._serializer_table["DataModelSeries"] = DataModelSeries

        self._zero_client._deserializer_table["ReferenceDatasetLongitudinal"] = ReferenceDatasetLongitudinal
        self._zero_client._deserializer_table["ReferenceDatasetTabular"] = ReferenceDatasetTabular
        self._zero_client._deserializer_table["ReferenceDataFrame"] = ReferenceDataFrame
        self._zero_client._deserializer_table["ReferenceSeries"] = ReferenceSeries
        self._zero_client._deserializer_table["DataModelTabular"] = DataModelTabular
        self._zero_client._deserializer_table["DataModelLongitudinal"] = DataModelLongitudinal
        self._zero_client._deserializer_table["DataModelDataFrame"] = DataModelDataFrame
        self._zero_client._deserializer_table["DataModelSeries"] = DataModelSeries

    def call(self, safe_function_class: Type, *arguments_list, **arguments_dict):
        # TODO this only deals with args, should also deal with kvargs
        check_instance(safe_function_class, Type)
        safe_function_class_name = str(safe_function_class).split(".")[-1][:-2]
        return self._zero_client.call(safe_function_class_name, *arguments_list, **arguments_dict)
