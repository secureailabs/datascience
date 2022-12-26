import sys

from sail_safe_functions.aggregator.data_model.data_model_data_frame import DataModelDataFrame
from sail_safe_functions.aggregator.data_model.data_model_longitudinal import DataModelLongitudinal
from sail_safe_functions.aggregator.data_model.data_model_series import DataModelSeries
from sail_safe_functions.aggregator.data_model.data_model_tabular import DataModelTabular
from sail_safe_functions.aggregator.reference_data_frame import ReferenceDataFrame
from sail_safe_functions.aggregator.reference_dataset_longitudinal import ReferenceDatasetLongitudinal
from sail_safe_functions.aggregator.reference_dataset_tabular import ReferenceDatasetTabular
from sail_safe_functions.aggregator.reference_series import ReferenceSeries
from zero import ZeroClient

if __name__ == "__main__":
    # Specific aguments
    hostname = "127.0.0.1"
    port = 5001
    dataset_id = "a892ef90-4f6f-11ed-bdc3-0242ac120002"

    client = ZeroClient(hostname, port)

    client._serializer_table["ReferenceDatasetLongitudinal"] = ReferenceDatasetLongitudinal
    client._serializer_table["ReferenceDatasetTabular"] = ReferenceDatasetTabular
    client._serializer_table["ReferenceDataFrame"] = ReferenceDataFrame
    client._serializer_table["ReferenceSeries"] = ReferenceSeries
    client._serializer_table["DataModelTabular"] = DataModelTabular
    client._serializer_table["DataModelLongitudinal"] = DataModelLongitudinal
    client._serializer_table["DataModelDataFrame"] = DataModelDataFrame
    client._serializer_table["DataModelSeries"] = DataModelSeries

    client._deserializer_table["ReferenceDatasetLongitudinal"] = ReferenceDatasetLongitudinal
    client._deserializer_table["ReferenceDatasetTabular"] = ReferenceDatasetTabular
    client._deserializer_table["ReferenceDataFrame"] = ReferenceDataFrame
    client._deserializer_table["ReferenceSeries"] = ReferenceSeries
    client._deserializer_table["DataModelTabular"] = DataModelTabular
    client._deserializer_table["DataModelLongitudinal"] = DataModelLongitudinal
    client._deserializer_table["DataModelDataFrame"] = DataModelDataFrame
    client._deserializer_table["DataModelSeries"] = DataModelSeries

    result = client.call("ReadDatasetFhirv1Precompute", dataset_id)

    print(result)
