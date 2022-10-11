from sail_safe_functions_orchestrator.data_model.data_model_data_frame import DataModelDataFrame
from sail_safe_functions_orchestrator.data_model.data_model_series import DataModelSeries
from sail_safe_functions_orchestrator.data_model.data_model_tabular import DataModelTabular
from sail_safe_functions_orchestrator.client_rpc_zero import ClientRPCZero
from sail_safe_functions_orchestrator.service_client_dict import ServiceClientDict
from sail_safe_functions_orchestrator import preprocessing

from sail_safe_functions_orchestrator.preprocessing import convert
from sail_safe_functions_orchestrator import statistics

if __name__ == "__main__":

    # Specific aguments
    # 20_1
    # a892ef90-4f6f-11ed-bdc3-0242ac120002

    # 60_1
    # a892ffd0-4f6f-11ed-bdc3-0242ac120002
    # a89301b0-4f6f-11ed-bdc3-0242ac120002
    # a89302dc-4f6f-11ed-bdc3-0242ac120002

    
    list_dataset_id = []
    list_dataset_id.append("a892ffd0-4f6f-11ed-bdc3-0242ac120002")
    list_dataset_id.append("a89301b0-4f6f-11ed-bdc3-0242ac120002")
    #list_dataset_id.append("a89302dc-4f6f-11ed-bdc3-0242ac120002")
    list_port = []
    list_port.append(5001)
    list_port.append(5002)
    #list_port.append(12347)
    service_client = ServiceClientDict()
    for dataset_id, port in zip(list_dataset_id, list_port):
        service_client.register_client(dataset_id, ClientRPCZero("127.0.0.1", port))

    # Arrange
    dataset_federation_id = "a892f738-4f6f-11ed-bdc3-0242ac120002"
    dataset_federation_name = "r4sep2019_csvv1_20_1"
    data_frame_name = "data_frame_0"

    data_model_data_frame = DataModelDataFrame(data_frame_name)
    data_model_data_frame.add_data_model_series(
        DataModelSeries.create_numerical(
            series_name="bmi_mean",
            measurement_source_name="Observation:Body Mass Index",
            type_agregator=DataModelSeries.AgregatorIntervalMean,
            unit="kg/m2",
        )
    )
    data_model_data_frame.add_data_model_series(
        DataModelSeries.create_numerical(
            series_name="bmi_first",
            measurement_source_name="Observation:Body Mass Index",
            type_agregator=DataModelSeries.AgregatorIntervalFirstOccurance,
            unit="kg/m2",
        )
    )

    data_model_data_frame.add_data_model_series(
        DataModelSeries.create_numerical(
            series_name="bmi_last",
            measurement_source_name="Observation:Body Mass Index",
            type_agregator=DataModelSeries.AgregatorIntervalLastOccurance,
            unit="kg/m2",
        )
    )
    data_model_tablular = DataModelTabular()
    data_model_tablular.add_data_model_data_frame(data_model_data_frame)
    
    # act
    dataset_longitudinal = preprocessing.read_dataset_fhirv1(service_client, list_dataset_id)
    dataset_tabular = convert.convert_to_dataset_tabular(
        dataset_longitudinal, dataset_federation_id, dataset_federation_name, data_model_tablular
    )
    data_frame_nan = dataset_tabular[data_frame_name]
    name_series_1 = data_frame_nan.list_series_name[1]
    print(statistics.count(data_frame_nan[name_series_1]))
    data_frame_nonan = preprocessing.drop_missing(
        data_frame_nan, axis=0, how="any", thresh=None, subset=None
    )
    print(statistics.count(data_frame_nonan[name_series_1]))
    series_1 = data_frame_nonan[name_series_1]
    mean_1 = statistics.mean(series_1)
    print(mean_1)