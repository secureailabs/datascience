<<<<<<< HEAD
import json
import os

from sail_safe_functions_orchestrator.data_frame_federated import DataFrameFederated
from sail_safe_functions_test.helper_sail_safe_functions.data_frame_federated_local import DataFrameFederatedLocal
from sail_safe_functions_test.helper_sail_safe_functions.data_frame_federated_source_jsonzip_local import (
    DataFrameFederatedSourceJsonzipLocal,
)
=======
import os

from sail_safe_functions_orchestrator.dataframe_federated import DataframeFederated
from sail_safe_functions_test.helper_sail_safe_functions.dataframe_federated_local import DataframeFederatedLocal
>>>>>>> 5759326b8e4fb0a8cedbf5b339ee9d6da334a584


class ToolsTestData:
    @staticmethod
<<<<<<< HEAD
    def list_data() -> dict:
=======
    def list_data():
>>>>>>> 5759326b8e4fb0a8cedbf5b339ee9d6da334a584
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
<<<<<<< HEAD
        dict_dataset["data_jsonzip_fhir_r4_sep2019"]["schema"] = {}
        dict_dataset["data_jsonzip_fhir_r4_sep2019"]["schema"]["race_cholesterol"] = "schema_race_cholesterol.json"
=======
        dict_dataset["data_jsonzip_fhir_r4_sep2019"]["schema"] = "schema_population_0.json"
>>>>>>> 5759326b8e4fb0a8cedbf5b339ee9d6da334a584
        dict_dataset["data_jsonzip_fhir_r4_sep2019"]["dataset"] = {}
        dict_dataset["data_jsonzip_fhir_r4_sep2019"]["dataset"]["1"] = [
            "dataset_0.zip",
            "dataset_1.zip",
            "dataset_2.zip",
        ]
        return dict_dataset

    @staticmethod
<<<<<<< HEAD
    def load_test_data_frame_csv(
        name_dataset: str, name_table: str = None, blob_connection_string: str = None
    ) -> DataFrameFederated:
=======
    def load_test_dataframe_csv(
        name_dataset: str, name_table: str = None, blob_connection_string: str = None
    ) -> DataframeFederated:
>>>>>>> 5759326b8e4fb0a8cedbf5b339ee9d6da334a584

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
<<<<<<< HEAD
        data_frame = DataFrameFederatedLocal()
=======
        data_frame = DataframeFederatedLocal()
>>>>>>> 5759326b8e4fb0a8cedbf5b339ee9d6da334a584
        list_name_file_csv = dict_dataset[name_dataset]["dataset"][name_table]
        for name_file_csv in list_name_file_csv:
            path_file_csv = os.path.join(path_dir_dataset, name_file_csv)
            data_frame.add_csv(path_file_csv)

        return data_frame

    @staticmethod
<<<<<<< HEAD
    def load_schema(name_data_federation: str, name_schema: str, blob_connection_string: str = None) -> dict:
        path_dir_test_data = os.environ.get("PATH_SAIL_TEST_DATA")
        if path_dir_test_data is None:
            raise RuntimeError("`PATH_SAIL_TEST_DATA` not set!")

        dict_dataset = ToolsTestData.list_data()
        if name_data_federation not in dict_dataset:
            raise ValueError(f"Unknown name_data_federation: {name_data_federation}")
        path_dir_dataset = os.path.join(path_dir_test_data, name_data_federation)

        if name_schema not in dict_dataset[name_data_federation]["schema"]:
            raise ValueError(f"Unknown name_schema: {name_schema}")
        path_file_schema = os.path.join(path_dir_dataset, dict_dataset[name_data_federation]["schema"][name_schema])

        with open(path_file_schema, "r") as file:
            return json.load(file)

    @staticmethod
    def load_data_frame_source_jsonzip(
        name_data_federation: str, name_dataset: str, blob_connection_string: str = None
    ) -> DataFrameFederated:
=======
    def load_test_dataframe_jsonzip(
        name_dataset: str, name_table: str, blob_connection_string: str = None
    ) -> DataframeFederated:
>>>>>>> 5759326b8e4fb0a8cedbf5b339ee9d6da334a584

        path_dir_test_data = os.environ.get("PATH_SAIL_TEST_DATA")
        if path_dir_test_data is None:
            raise RuntimeError("`PATH_SAIL_TEST_DATA` not set!")

        dict_dataset = ToolsTestData.list_data()
<<<<<<< HEAD
        if name_data_federation not in dict_dataset:
            raise ValueError(f"Unknown name_data_federation: {name_data_federation}")

        if name_dataset is not None:
            if not name_dataset not in dict_dataset[name_data_federation]:
                raise ValueError(f"Unknown name_dataset: {name_dataset}")
        else:
            name_dataset = list(dict_dataset[name_dataset].keys())[0]

        path_dir_dataset = os.path.join(path_dir_test_data, name_data_federation)

        list_path_file_jsonzip = [
            os.path.join(path_dir_dataset, name_file)
            for name_file in dict_dataset[name_data_federation]["dataset"][name_dataset]
        ]
        return DataFrameFederatedSourceJsonzipLocal(list_path_file_jsonzip)

    def temp_create_schema():

        dict_column_template = {}
        dict_column_template["gender"] = {}
        dict_column_template["gender"]["type_feature"] = "patient_gender"

        dict_column_template["race"] = {}
        dict_column_template["race"]["type_feature"] = "patient_race"

        dict_column_template["ethnicity"] = {}
        dict_column_template["ethnicity"]["type_feature"] = "patient_ethnicity"

        dict_column_template["marital_status"] = {}
        dict_column_template["marital_status"]["type_feature"] = "patient_marital_status"

        dict_column_template["first_height"] = {}
        dict_column_template["first_height"]["type_feature"] = "numeric"
        dict_column_template["first_height"]["name_measurement"] = "Observation:Body Height"
        dict_column_template["first_height"]["type_selector"] = "first_occurance"

        dict_column_template["last_height"] = {}
        dict_column_template["last_height"]["type_feature"] = "numeric"
        dict_column_template["last_height"]["name_measurement"] = "Observation:Body Height"
        dict_column_template["last_height"]["type_selector"] = "last_occurance"

        dict_column_template["last_bmi"] = {}
        dict_column_template["last_bmi"]["type_feature"] = "numeric"
        dict_column_template["last_bmi"]["name_measurement"] = "Observation:Body Height"
        dict_column_template["last_bmi"]["type_selector"] = "count_occurance"

        dict_column_template["mean_cholesterol"] = {}
        dict_column_template["mean_cholesterol"]["type_feature"] = "numeric"
        dict_column_template["mean_cholesterol"]["name_measurement"] = "Observation:Total Cholesterol"
        dict_column_template["mean_cholesterol"]["type_selector"] = "mean"

        dict_column_template["first_influenza"] = {}
        dict_column_template["first_influenza"]["type_feature"] = "categorical"
        dict_column_template["first_influenza"][
            "name_measurement"
        ] = "Immunization:Influenza, seasonal, injectable, preservative free"
        dict_column_template["first_influenza"]["type_selector"] = "first_occurance"

        dict_column_template["last_smoking"] = {}
        dict_column_template["last_smoking"]["type_feature"] = "categorical"
        dict_column_template["last_smoking"]["name_measurement"] = "Observation:Tobacco smoking status NHIS"
        dict_column_template["last_smoking"]["type_selector"] = "last_occurance"
        schema = {}
        schema["dict_column"] = dict_column_template
        schema["list_name_column"] = sorted(list(dict_column_template.keys()))
        return schema
=======
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
>>>>>>> 5759326b8e4fb0a8cedbf5b339ee9d6da334a584
