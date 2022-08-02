import os

from sail_safe_functions_orchestrator.dataframe_federated import DataframeFederated
from sail_safe_functions_test.helper_sail_safe_functions.dataframe_federated_local import DataframeFederatedLocal


class ToolsTestData:
    @staticmethod
    def list_data():
        dict_dataset = {}
        dict_dataset["data_csv_investor_demo"] = {}
        dict_dataset["data_csv_investor_demo"]["dataset"] = {}
        dict_dataset["data_csv_investor_demo"]["dataset"]["1"] = ["bmc1.csv", "bwh1.csv", "mgh1.csv"]
        dict_dataset["data_csv_investor_demo"]["dataset"]["2"] = ["bmc2.csv", "bwh2.csv", "mgh2.csv"]
        dict_dataset["data_csv_investor_demo"]["dataset"]["3"] = ["bmc3.csv", "bwh3.csv", "mgh3.csv"]
        dict_dataset["data_csv_kidney"] = {}
        dict_dataset["data_csv_kidney"]["dataset"] = {}
        dict_dataset["data_csv_kidney"]["dataset"]["1"] = ["kidney_disease.csv"]
        dict_dataset["data_csv_kidney_clean"] = {}
        dict_dataset["data_csv_kidney_clean"]["schema"] = "schema.json"
        dict_dataset["data_csv_kidney_clean"]["dataset"] = {}
        dict_dataset["data_csv_kidney_clean"]["dataset"]["1"] = ["kidney_disease_clean.csv"]
        dict_dataset["data_jsonzip_fhir_r4_sep2019"] = {}
        dict_dataset["data_jsonzip_fhir_r4_sep2019"]["schema"] = "schema_population_0.json"
        dict_dataset["data_jsonzip_fhir_r4_sep2019"]["dataset"] = {}
        dict_dataset["data_jsonzip_fhir_r4_sep2019"]["dataset"]["1"] = [
            "dataset_0.zip",
            "dataset_1.zip",
            "dataset_2.zip",
        ]
        return dict_dataset

    @staticmethod
    def load_test_dataframe_csv(
        name_dataset: str, name_table: str = None, blob_connection_string: str = None
    ) -> DataframeFederated:

        path_dir_test_data = os.environ.get("PATH_SAIL_TEST_DATA")
        if path_dir_test_data is None:
            raise RuntimeError("`PATH_SAIL_TEST_DATA` not set!")

        dict_dataset = ToolsTestData.list_data()
        if name_dataset not in dict_dataset:
            raise ValueError(f"Unknown name_dataset: {name_dataset}")

        if name_table is not None:
            if name_table not in dict_dataset[name_dataset]["dataset"]:
                raise ValueError(f"Unknown name_table: {name_table}")
        else:
            name_table = list(dict_dataset[name_dataset]["dataset"].keys())[0]

        path_dir_dataset = os.path.join(path_dir_test_data, name_dataset)
        data_frame = DataframeFederatedLocal()
        list_name_file_csv = dict_dataset[name_dataset]["dataset"][name_table]
        for name_file_csv in list_name_file_csv:
            path_file_csv = os.path.join(path_dir_dataset, name_file_csv)
            data_frame.add_csv(path_file_csv)

        return data_frame

    @staticmethod
    def load_test_dataframe_jsonzip(
        name_dataset: str, name_table: str, blob_connection_string: str = None
    ) -> DataframeFederated:

        path_dir_test_data = os.environ.get("PATH_SAIL_TEST_DATA")
        if path_dir_test_data is None:
            raise RuntimeError("`PATH_SAIL_TEST_DATA` not set!")

        dict_dataset = ToolsTestData.list_data()
        if name_dataset not in dict_dataset:
            raise ValueError(f"Unknown name_dataset: {name_dataset}")

        if name_table is not None:
            if not name_table not in dict_dataset[name_dataset]:
                raise ValueError(f"Unknown name_table: {name_table}")
        else:
            name_table = list(dict_dataset[name_dataset].keys())[0]

        path_dir_dataset = os.path.join(path_dir_test_data, "" + name_dataset)
        data_frame = DataframeFederatedLocal()
        list_name_file_csv = dict_dataset[name_dataset][name_table]
        for name_file_csv in list_name_file_csv:
            path_file_csv = os.path.join(path_dir_dataset, name_file_csv)
            data_frame.add_csv(path_file_csv)

        return data_frame
