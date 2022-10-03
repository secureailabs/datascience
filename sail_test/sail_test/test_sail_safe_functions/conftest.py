"""
Pytest fixtures
"""
import os
from typing import List, Tuple, Type

import numpy as np
import pandas as pd
import pytest
from config import DATA_PATH, PORT1, PORT2, PORT3, VMIP
from sail_orchestrator_lib.data import utils
from zero import ZeroClient


@pytest.fixture
def connect_to_three_VMs() -> List[Type[ZeroClient]]:
    """
    connect to three virtual machines

    :return: A list of three cliens
    :rtype: Type[ZeroClient]
    """
    client1 = ZeroClient(VMIP, PORT1)
    client2 = ZeroClient(VMIP, PORT2)
    client3 = ZeroClient(VMIP, PORT3)
    return [client1, client2, client3]


@pytest.fixture
def connect_to_one_VM() -> Type[ZeroClient]:
    """
    Connect to one virtual machine

    :return: A RPC client for remote function/object operation
    :rtype: Client
    """
    client = ZeroClient(VMIP, PORT1)
    return client


@pytest.fixture
def tuple_kidney_schema_dataframe(
    connect_to_one_VM,
):
    """
    Fixture for loading a dataframe without missing values and a matching schema

    :return: tuple_kidney_schema_dataframe: A tuple iwth a dataframe and a matching schema
    :rtype: class : Tuple[dict, DataFrameFederatedLocal]
    """
    # path_file_json = f"{DATA_PATH}/data_csv_kidney_clean/schema.json"
    # path_file_csv = f"{DATA_PATH}/data_csv_kidney_clean/kidney_disease_clean.csv"

    # schema = utils.load_schema(connect_to_one_VM, path_file_csv)
    # rdf = utils.load_df_from_csv(connect_to_one_VM, path_file_csv)
    # dataframe = DataFrameFederated()
    # dataframe.add(rdf)
    # return (schema, dataframe)
    return (None, None)


@pytest.fixture
def data_frame_federated_kidney(
    connect_to_one_VM,
):
    """
    Fixture for loading a dataframe with missing values
    :return: data_frame_federated_kidney: a federated dataframe
    :rtype: class : DataFrameFederatedLocal
    """

    # path_file_csv = f"{DATA_PATH}/data_csv_kidney/kidney_disease.csv"
    # rdf = utils.load_df_from_csv(connect_to_one_VM, path_file_csv)

    # data_frame_federated_kidney = DataFrameFederated()
    # data_frame_federated_kidney.add(rdf)
    # return data_frame_federated_kidney
    return None


@pytest.fixture
def dataframe_kidney() -> pd.DataFrame:
    """
    Fixture for loading a dataframe with some missing values

    :return: dataframe_kidney: A dataframe with some missing fields
    :rtype: class : pd.DataFrame
    """

    # path_file_csv = os.path.join(DATA_PATH, "data_csv_kidney", "kidney_disease.csv")
    # return pd.read_csv(path_file_csv)
    return None


@pytest.fixture
def dataframe_kidney_clean() -> pd.DataFrame:
    """
    Fixture for loading a dataframe with no missing values

    :return: dataframe_kidney_clean: A dataframe with no missing fields
    :rtype: class : pd.DataFrame
    """

    # path_file_csv = os.path.join(DATA_PATH, "data_csv_kidney_clean", "kidney_disease_clean.csv")
    # return pd.read_csv(path_file_csv)
    return None


@pytest.fixture
def scheme_kidney() -> dict:
    """
    Fixture for loading the scheme for kidney dataset

    :return: scheme_kidney: Scheme is associated with the kidney dataset
    :rtype: class : dict
    """

    # path_file_json = os.path.join(DATA_PATH, "data_csv_kidney_clean", "schema.json")
    # file = open(path_file_json, "r")
    # schema_content = file.read()
    # return json.loads(schema_content)
    return None


@pytest.fixture
def one_sample_big_remote(
    connect_to_three_VMs,
) -> List:
    """
    Fixture for SeriesFederatedLocal with this first part of the investor demo dataset

    :return: DataFrameFederatedLocal
    :rtype: class : test_sail_safe_functions.series_federated_local.SeriesFederatedLocal
    """
    list_name_file_csv = ["bmc1.csv", "bwh1.csv", "mgh1.csv"]
    id_column_0 = "PD-L1 level before treatment"

    series_federated = []
    for i in range(len(list_name_file_csv)):
        path_file_csv = f"{DATA_PATH}/data_csv_investor_demo/{list_name_file_csv[i]}"
        rdf = utils.load_df_from_csv(connect_to_three_VMs[i], path_file_csv)
        series_federated.append(rdf[id_column_0])

    return series_federated


@pytest.fixture
def two_sample_big_remote(
    connect_to_three_VMs,
) -> Tuple[List, List]:
    """
    Fixture for SeriesFederatedLocal with this first part of the investor demo dataset

    :return: DataFrameFederatedLocal
    :rtype: class : test_sail_safe_functions.series_federated_local.SeriesFederatedLocal
    """
    list_name_file_csv = ["bmc1.csv", "bwh1.csv", "mgh1.csv"]
    id_column_0 = "PD-L1 level before treatment"
    id_column_1 = "PD-L1 level after treatment"

    series_federated_1 = []
    series_federated_2 = []
    for i in range(len(list_name_file_csv)):
        path_file_csv = f"{DATA_PATH}/data_csv_investor_demo/{list_name_file_csv[i]}"
        rdf = utils.load_df_from_csv(connect_to_three_VMs[i], path_file_csv)
        series_federated_1.append(rdf[id_column_0])
        series_federated_2.append(rdf[id_column_1])

    return (series_federated_1, series_federated_2)


@pytest.fixture
def two_sample_categorical_remote(
    connect_to_one_VM,
) -> Tuple[List, List]:
    """
    Fixture for SeriesFederatedLocal with this first part of the kidney disease dataset

    :return: DataFrameFederatedLocal
    :rtype: class : test_sail_safe_functions.series_federated_local.SeriesFederatedLocal
    """
    list_name_file_csv = ["kidney_disease_clean.csv"]
    id_column_0 = "rbc"
    id_column_1 = "classification"

    series_federated_1 = []
    series_federated_2 = []

    for name_file_csv in list_name_file_csv:
        path_file_csv = f"{DATA_PATH}/data_csv_kidney_clean/{name_file_csv}"
        rdf = utils.load_df_from_csv(connect_to_one_VM, path_file_csv)
        series_federated_1.append(rdf[id_column_0])
        series_federated_2.append(rdf[id_column_1])

    return (series_federated_1, series_federated_2)


# to do
@pytest.fixture
def two_sample_small_remote(
    connect_to_one_VM,
) -> Tuple[List, List]:
    """
    A two sample tuple with data from wikipedia

    :return: SeriesFederatedLocal
    :rtype: class : test_sail_safe_functions.series_federated_local.SeriesFederatedLocal
    """
    sample_0_list = [
        17.2,
        20.9,
        22.6,
        18.1,
        21.7,
        21.4,
        23.5,
        24.2,
        14.7,
        21.8,
    ]
    sample_1_list = [
        21.5,
        22.8,
        21.0,
        23.0,
        21.6,
        23.6,
        22.5,
        20.7,
        23.4,
        21.8,
        20.7,
        21.7,
        21.5,
        22.5,
        23.6,
        21.5,
        22.5,
        23.5,
        21.5,
        21.8,
    ]

    client = connect_to_one_VM

    sample_0_numpy = utils.array(client, sample_0_list)
    sample_1_numpy = utils.array(client, sample_1_list)

    sample_0 = [client.proxy("RemoteSeries", sample_0_numpy)]
    sample_1 = [client.proxy("RemoteSeries", sample_1_numpy)]
    return (sample_0, sample_1)


@pytest.fixture
def two_sample_small_two_remote(
    connect_to_one_VM,
) -> Tuple[List, List]:
    """
    A two sample tuple with data from wikipedia

    :return: SeriesFederatedLocal
    :rtype: class : test_sail_safe_functions.series_federated_local.SeriesFederatedLocal
    """
    client = connect_to_one_VM

    sample_0_numpy = utils.array(client, [14, 34, 16, 43, 45, 36, 42, 43, 16, 27])
    sample_1_numpy = utils.array(client, [34, 36, 44, 18, 42, 39, 16, 35, 15, 33])

    sample_0 = [client.proxy("RemoteSeries", sample_0_numpy)]
    sample_1 = [client.proxy("RemoteSeries", sample_1_numpy)]
    return (sample_0, sample_1)


@pytest.fixture
def two_sample_small_paired_remote(
    connect_to_one_VM,
) -> Tuple[List, List]:
    """
    A two sample tuple with data from https://en.wikipedia.org/wiki/Student%27s_t-test#Dependent_t-test_for_paired_samples

    :return: SeriesFederatedLocal
    :rtype: class : test_sail_safe_functions.series_federated_local.SeriesFederatedLocal
    """
    client = connect_to_one_VM

    sample_0_numpy = utils.array(client, [30.02, 29.99, 30.11, 29.97, 30.01, 29.99])
    sample_1_numpy = utils.array(client, [29.89, 29.93, 29.72, 29.98, 30.02, 29.98])

    sample_0 = [client.proxy("RemoteSeries", sample_0_numpy)]
    sample_1 = [client.proxy("RemoteSeries", sample_1_numpy)]
    return (sample_0, sample_1)


@pytest.fixture
def one_sample_normal_remote(
    connect_to_one_VM,
) -> List:
    client = connect_to_one_VM

    sample_0_numpy = utils.random_normal(client, 0, 1, 17, 42)

    sample_0 = [client.proxy("RemoteSeries", sample_0_numpy)]
    return sample_0


@pytest.fixture
def two_sample_normal_remote(
    connect_to_one_VM,
) -> List:
    client = connect_to_one_VM

    sample_0_numpy = utils.random_normal(client, 0, 1, 200, 42)
    sample_1_numpy = utils.random_normal(client, 0, 1, 200, 24)

    return ([client.proxy("RemoteSeries", sample_0_numpy)], [client.proxy("RemoteSeries", sample_1_numpy)])


@pytest.fixture
def one_sample_big_local() -> List:
    """
    Fixture for SeriesFederatedLocal with this first part of the investor demo dataset
    :return: DataFrameFederatedLocal
    :rtype: class : test_sail_safe_functions.series_federated_local.SeriesFederatedLocal
    """
    list_name_file_csv = ["bmc1.csv", "bwh1.csv", "mgh1.csv"]
    id_column_0 = "PD-L1 level before treatment"

    series = pd.Series()
    for name_file_csv in list_name_file_csv:
        path_file_csv = os.path.join(DATA_PATH, "data_csv_investor_demo", name_file_csv)
        df = pd.read_csv(path_file_csv)
        series = pd.concat([series, df[id_column_0]])

    return series


@pytest.fixture
def two_sample_big_local() -> Tuple[List, List]:
    """
    Fixture for SeriesFederatedLocal with this first part of the investor demo dataset
    :return: DataFrameFederatedLocal
    :rtype: class : test_sail_safe_functions.series_federated_local.SeriesFederatedLocal
    """
    list_name_file_csv = ["bmc1.csv", "bwh1.csv", "mgh1.csv"]
    id_column_0 = "PD-L1 level before treatment"
    id_column_1 = "PD-L1 level after treatment"

    series_1 = pd.Series()
    series_2 = pd.Series()
    for name_file_csv in list_name_file_csv:
        path_file_csv = os.path.join(DATA_PATH, "data_csv_investor_demo", name_file_csv)
        df = pd.read_csv(path_file_csv)
        series_1 = pd.concat([series_1, df[id_column_0]])
        series_2 = pd.concat([series_2, df[id_column_1]])

    return (series_1, series_2)


@pytest.fixture
def two_sample_categorical_local() -> Tuple[pd.Series, pd.Series]:
    """
    Fixture for SeriesFederatedLocal with this first part of the kidney disease dataset
    :return: DataFrameFederatedLocal
    :rtype: class : test_sail_safe_functions.series_federated_local.SeriesFederatedLocal
    """
    name_file_csv = "kidney_disease_clean.csv"
    id_column_0 = "rbc"
    id_column_1 = "classification"

    path_file_csv = os.path.join(DATA_PATH, "data_csv_kidney_clean", name_file_csv)
    df = pd.read_csv(path_file_csv)
    series_1 = df[id_column_0]
    series_2 = df[id_column_1]

    return (series_1, series_2)


@pytest.fixture
def two_sample_small_local() -> Tuple[List, List]:
    """
    A two sample tuple with data from wikipedia
    :return: SeriesFederatedLocal
    :rtype: class : test_sail_safe_functions.series_federated_local.SeriesFederatedLocal
    """
    sample_0_numpy = np.array(
        [
            17.2,
            20.9,
            22.6,
            18.1,
            21.7,
            21.4,
            23.5,
            24.2,
            14.7,
            21.8,
        ]
    )
    sample_1_numpy = np.array(
        [
            21.5,
            22.8,
            21.0,
            23.0,
            21.6,
            23.6,
            22.5,
            20.7,
            23.4,
            21.8,
            20.7,
            21.7,
            21.5,
            22.5,
            23.6,
            21.5,
            22.5,
            23.5,
            21.5,
            21.8,
        ]
    )

    return (sample_0_numpy, sample_1_numpy)


@pytest.fixture
def two_sample_small_two_local() -> Tuple[List, List]:
    """
    A two sample tuple with data from wikipedia
    :return: SeriesFederatedLocal
    :rtype: class : test_sail_safe_functions.series_federated_local.SeriesFederatedLocal
    """
    sample_0_numpy = np.array([14, 34, 16, 43, 45, 36, 42, 43, 16, 27])
    sample_1_numpy = np.array([34, 36, 44, 18, 42, 39, 16, 35, 15, 33])

    return (sample_0_numpy, sample_1_numpy)


@pytest.fixture
def two_sample_small_paired_local() -> Tuple[List, List]:
    """
    A two sample tuple with data from https://en.wikipedia.org/wiki/Student%27s_t-test#Dependent_t-test_for_paired_samples
    :return: SeriesFederatedLocal
    :rtype: class : test_sail_safe_functions.series_federated_local.SeriesFederatedLocal
    """
    sample_0_numpy = np.array([30.02, 29.99, 30.11, 29.97, 30.01, 29.99])
    sample_1_numpy = np.array([29.89, 29.93, 29.72, 29.98, 30.02, 29.98])

    return (sample_0_numpy, sample_1_numpy)


@pytest.fixture
def one_sample_normal_local() -> List:

    np.random.seed(42)
    array_sample_0 = np.random.normal(0, 1, 17)  # works from size 17 onwards

    return array_sample_0


@pytest.fixture
def two_sample_normal_local() -> List:

    np.random.seed(42)
    array_sample_0 = np.random.normal(0, 1, 200)
    array_sample_1 = np.random.normal(0, 1, 200)

    return (array_sample_0, array_sample_1)
