import os

from sail_safe_functions_orchestrator.packager_dataset.packager_data_federation import PackagerDataFederation

if __name__ == "__main__":
    path_dir_data_federation_packaged = "C:\\data\\formatted\\data_federation_packaged"
    list_name_file = os.listdir(path_dir_data_federation_packaged)
    set_id = set()
    for name_file in list_name_file:
        print(name_file)
        path_file_data_federation_source = os.path.join(path_dir_data_federation_packaged, name_file)
        packager = PackagerDataFederation()
        header = packager.get_data_federation_packaged_header(path_file_data_federation_source)
        data_federation_name = header["data_federation_name"]
        data_federation_id = header["data_federation_id"]
        if data_federation_id in set_id:
            print(f"duplicate id {data_federation_id}")
        set_id.add(data_federation_id)
        print(f"    {data_federation_name.ljust(24)} {data_federation_id}")
        dict_dataset_name_to_dataset_id = packager.get_dict_dataset_name_to_dataset_id(path_file_data_federation_source)
        for dataset_name, dataset_id in dict_dataset_name_to_dataset_id.items():
            if dataset_id in set_id:
                print(f"        {dataset_name.ljust(20)} {dataset_id} duplicate")
            else:
                print(f"        {dataset_name.ljust(20)} {dataset_id}")
            set_id.add(dataset_id)
        packager.prepare_data_federation(path_file_data_federation_source)
