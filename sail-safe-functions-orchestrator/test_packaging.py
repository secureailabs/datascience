from sail_safe_functions_orchestrator.tools_common.tools_dataset_packaging import ToolsDatasetPackaging

path_dir_data_federation_unpackaged = "/home/jaap/data/data_federation_unpackaged"
path_dir_data_federation_packaged = "/home/jaap/data/data_federation_packaged"
data_federation_id = "r4sep2019_fhirv1_20_1"
ToolsDatasetPackaging.fhirv1_package_data_federation(
    path_dir_data_federation_unpackaged, path_dir_data_federation_packaged, data_federation_id
)
