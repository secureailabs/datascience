from sail_safe_functions_orchestrator import statistics
from sail_safe_functions_orchestrator.data_model.data_model_data_frame import DataModelDataFrame
from sail_safe_functions_orchestrator.data_model.data_model_series import DataModelSeries
from sail_safe_functions_orchestrator.data_model.data_model_tabular import DataModelTabular
from sail_safe_functions_orchestrator.dataset_longitudinal_federated import DatasetLongitudinalFederated
from sail_safe_functions_orchestrator.preprocessing import convert
from sail_safe_functions_orchestrator.statistics.mean import Mean

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
dataset_longitudinal = DatasetLongitudinalFederated.read_for_path_file(path_file_data_federation)

dataset_tabular = convert.convert_to_dataset_tabular(
    dataset_longitudinal, dataset_federation_id, dataset_federation_name, data_model_tablular
)

print("check data model")
name_series_1 = dataset_tabular[data_frame_name].list_series_name[1]
name_series_2 = dataset_tabular[data_frame_name].list_series_name[2]
print(type(dataset_tabular))
print(type(dataset_tabular[data_frame_name]))
print(type(dataset_tabular[data_frame_name][name_series_1]))
print(dataset_tabular[data_frame_name][name_series_1].data_model_series.type_data_level)
print(dataset_tabular[data_frame_name][name_series_1].data_model_series.unit)


print(name_series_1)
print(name_series_2)
series_1 = dataset_tabular[data_frame_name][name_series_1]
series_2 = dataset_tabular[data_frame_name][name_series_2]
print(statistics.mean(series_1))
print(statistics.mean(series_2))
