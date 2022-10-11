import os

from sail_safe_functions_orchestrator.packager_dataset.packager_data_federation import PackagerDataFederation
if __name__ == "__main__":
    path_dir_data_federation_unpackaged = "C:\\data\\formatted\\data_federation_unpackaged"
    path_dir_data_federation_packaged = "C:\\data\\formatted\\data_federation_packaged"
    list_name_file = os.listdir(path_dir_data_federation_unpackaged)
    set_id = set()
    for name_file in list_name_file:
        print(name_file)
        path_dir_data_federation_source = os.path.join(path_dir_data_federation_unpackaged, name_file)
        path_file_data_federation_target = os.path.join(path_dir_data_federation_packaged, name_file + ".zip")
        packager = PackagerDataFederation()
        packager.package_data_federation(path_dir_data_federation_source, path_file_data_federation_target)
