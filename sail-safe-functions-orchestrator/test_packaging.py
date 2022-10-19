import json
import os
import sys

from sail_safe_functions_orchestrator.data_model_feature import DataModelFeature
from sail_safe_functions_orchestrator.data_model_tabular import DataModelTabular
from sail_safe_functions_orchestrator.packager_dataset.packager_data_federation import PackagerDataFederation
from sail_safe_functions_orchestrator.packager_dataset.serializer_dataset_csvv1 import SerializerDatasetCsvv1
from sail_safe_functions_orchestrator.packager_dataset.serializer_dataset_fhirv1 import SerializerDatasetFhirv1

# Arrange
path_dir_data_federation_unpackaged_root = "/home/jaap/data/data_federation_unpackaged"
path_dir_data_federation_packaged_root = "/home/jaap/data/data_federation_packaged"
path_dir_dataset_prepared = "/home/jaap/data/dataset_prepared"
data_federation_name = "r4sep2019_fhirv1_20_1"
# data_federation_name = "r4sep2019_fhirv1_1k_1"
# data_federation_name = "r4sep2019_fhirv1_1k_3"
dataset_name = "dataset_0"
path_file_target = "/home/jaap/data/cohort_0.csv"
path_dir_data_federation_unpackaged = os.path.join(path_dir_data_federation_unpackaged_root, data_federation_name)
path_file_data_federation_packaged = os.path.join(path_dir_data_federation_packaged_root, data_federation_name + ".zip")
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
dict_dataset_name_to_dataset_id = packager_data_federation.get_list_dataset_id(path_file_data_federation_packaged)
print("done list")
sys.stdout.flush()
path_dir_dataset = os.path.join(path_dir_dataset_prepared, dict_dataset_name_to_dataset_id[dataset_name])
dataset_longitudinal = serializar_fhirv1.read_dataset_for_path(path_dir_dataset)

# Assert
print(len(dataset_longitudinal.list_patient))

# Arrange
data_model_tablular = DataModelTabular()
data_model_table = DataModelTable()
data_model_table.add_data_model_feature(
    DataModelFeature.create_numerical(
        feature_name="bmi_mean",
        measurement_source_name="Observation:Body Mass Index",
        type_agregator=DataModelFeature.AgregatorIntervalMean,
    )
)
data_model_table.add_data_model_feature(
    DataModelFeature.create_numerical(
        feature_name="bmi_first",
        measurement_source_name="Observation:Body Mass Index",
        type_agregator=DataModelFeature.AgregatorIntervalFirstOccurance,
    )
)

data_model_table.add_data_model_feature(
    DataModelFeature.create_numerical(
        feature_name="bmi_last",
        measurement_source_name="Observation:Body Mass Index",
        type_agregator=DataModelFeature.AgregatorIntervalLastOccurance,
    )
)
data_frame_table = data_frame_longitudinal.convert_to_data_frame_table(data_model_table)
data_frame_table.to_csv(path_file_target)
SerializerDatasetCsvv1.save_data_federation(data_frame_table)
