from sail_safe_functions_orchestrator.data_frame_federated import DataFrameFederated
from sail_safe_functions_orchestrator.data_model.data_model_data_frame import DataModelDataFrame
from sail_safe_functions_orchestrator.data_model.data_model_series import DataModelSeries
from sail_safe_functions_orchestrator.data_model.data_model_tabular import DataModelTabular
from sail_safe_functions_orchestrator.dataset_longitudinal_federated_local import DatasetLongitudinalFederatedLocal
from sail_safe_functions_orchestrator.preprocessing import convert

# Arrange
path_file_data_federation = "/home/jaap/data/data_federation_packaged/r4sep2019_fhirv1_20_1.zip"
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
dataset_longitudinal = DatasetLongitudinalFederatedLocal.read_for_path_file(path_file_data_federation)

dataset_tabular = convert.convert_to_dataset_tabular(
    dataset_longitudinal, dataset_federation_id, dataset_federation_name, data_model_tablular
)

print("check data model")
name_series = dataset_tabular[data_frame_name].list_series_name[0]
print(type(dataset_tabular))
print(type(dataset_tabular[data_frame_name]))
print(type(dataset_tabular[data_frame_name][name_series]))
print(dataset_tabular[data_frame_name][name_series].data_model_series.type_data_level)
print(dataset_tabular[data_frame_name][name_series].data_model_series.unit)
