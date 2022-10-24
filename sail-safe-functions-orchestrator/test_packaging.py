import json
import os
import sys

from sail_safe_functions_orchestrator.data_model_data_frame import DataModelDataFrame
from sail_safe_functions_orchestrator.data_model_series import DataModelSeries
from sail_safe_functions_orchestrator.data_model_tabular import DataModelTabular
from sail_safe_functions_orchestrator.packager_dataset.packager_data_federation import PackagerDataFederation
from sail_safe_functions_orchestrator.packager_dataset.serializer_dataset_csvv1 import SerializerDatasetCsvv1
from sail_safe_functions_orchestrator.packager_dataset.serializer_dataset_fhirv1 import SerializerDatasetFhirv1

# Arrange
path_dir_data_federation_unpackaged_root = "/home/jaap/data/data_federation_unpackaged"
path_dir_data_federation_packaged_root = "/home/jaap/data/data_federation_packaged"
path_dir_dataset_prepared = "/home/jaap/data/dataset_prepared"
data_federation_logitudinal_name = "r4sep2019_fhirv1_20_1"
dataset_logitudinal_name = "dataset_0"

data_federation_tabular_id = "a892f738-4f6f-11ed-bdc3-0242ac120002"
data_federation_tabular_name = "r4sep2019_csvv1_20_1"
dataset_tabular_id = "a892f878-4f6f-11ed-bdc3-0242ac120002"
dataset_tabular_name = "dataset_0"

data_frame_name = "data_frame_0"

path_dir_data_federation_unpackaged = os.path.join(
    path_dir_data_federation_unpackaged_root, data_federation_logitudinal_name
)
path_file_data_federation_packaged = os.path.join(
    path_dir_data_federation_packaged_root, data_federation_logitudinal_name + ".zip"
)
path_file_data_federation_header = os.path.join(path_dir_data_federation_unpackaged, "data_federation_header.json")
if os.path.isfile(path_file_data_federation_packaged):
    os.remove(path_file_data_federation_packaged)
with open(path_file_data_federation_header, "r") as file:
    data_federation_id = json.load(file)["data_federation_id"]


packager_data_federation = PackagerDataFederation()
serializar_fhirv1 = SerializerDatasetFhirv1()
serializar_csvv1 = SerializerDatasetCsvv1()
# Act
packager_data_federation.package_data_federation(
    path_dir_data_federation_unpackaged, path_file_data_federation_packaged
)
packager_data_federation.prepare_data_federation(path_file_data_federation_packaged, path_dir_dataset_prepared)
print("getting list")
sys.stdout.flush()
dict_dataset_name_to_dataset_id = packager_data_federation.get_dict_dataset_id(path_file_data_federation_packaged)
print("done list")
sys.stdout.flush()
path_dir_dataset = os.path.join(path_dir_dataset_prepared, dict_dataset_name_to_dataset_id[dataset_logitudinal_name])
path_dir_dataset_tabular = os.path.join(path_dir_dataset_prepared, dataset_tabular_id)

# here starts platform code
dataset_longitudinal = serializar_fhirv1.read_dataset_for_path(path_dir_dataset)

# Assert
print(len(dataset_longitudinal.list_patient))

# Arrange
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
dataset_tabular = dataset_longitudinal.convert_to_dataset_tabular(
    data_federation_tabular_name,
    data_federation_tabular_id,
    dataset_tabular_name,
    dataset_tabular_id,
    data_model_tablular,
)

print("list_series_name")
print(list(dataset_tabular[data_frame_name].list_series_name))

# act
serializar_csvv1.write_dataset_tabular_for_path(path_dir_dataset_tabular, dataset_tabular)
dataset_tabular_reloaded = serializar_csvv1.read_dataset_for_path(path_dir_dataset_tabular)

# assert
print("are equal")
print(dataset_tabular_reloaded == dataset_tabular)

print("check data model")
name_series = dataset_tabular[data_frame_name].list_series_name[0]
print(type(dataset_tabular))
print(type(dataset_tabular[data_frame_name]))
print(type(dataset_tabular[data_frame_name][name_series]))
print(dataset_tabular[data_frame_name][name_series].data_model_series.type_data_level)
print(dataset_tabular[data_frame_name][name_series].data_model_series.unit)
