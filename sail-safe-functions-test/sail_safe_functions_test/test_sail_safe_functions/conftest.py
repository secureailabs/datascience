"""
Pytest fixtures
"""
import json
import os
from typing import List, Tuple, Type

import numpy as np
import pandas as pd
import pytest
from config import DATA_PATH, PORT1, PORT2, PORT3, VMIP
from sail_safe_functions_orchestrator.data import utils
from sklearn.datasets import load_iris
from sklearn.preprocessing import OneHotEncoder
from zero import ZeroClient, serializer_table


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
    path_file_json = f"{DATA_PATH}/data_csv_kidney_clean/schema.json"
    path_file_csv = f"{DATA_PATH}/data_csv_kidney_clean/kidney_disease_clean.csv"

    schema = utils.load_schema(connect_to_one_VM, path_file_json)
    rdf = utils.load_df_from_csv(connect_to_one_VM, path_file_csv)
    dataframe = DataFrameFederated()
    dataframe.add(rdf)
    return (schema, dataframe)


@pytest.fixture
def data_frame_federated_kidney(
    connect_to_one_VM,
):
    """
    Fixture for loading a dataframe with missing values
    :return: data_frame_federated_kidney: a federated dataframe
    :rtype: class : DataFrameFederatedLocal
    """

    path_file_csv = f"{DATA_PATH}/data_csv_kidney/kidney_disease.csv"
    rdf = utils.load_df_from_csv(connect_to_one_VM, path_file_csv)

    data_frame_federated_kidney = DataFrameFederated()
    data_frame_federated_kidney.add(rdf)
    return data_frame_federated_kidney


@pytest.fixture
def dataframe_kidney() -> pd.DataFrame:
    """
    Fixture for loading a dataframe with some missing values

    :return: dataframe_kidney: A dataframe with some missing fields
    :rtype: class : pd.DataFrame
    """

    path_file_csv = os.path.join(DATA_PATH, "data_csv_kidney", "kidney_disease.csv")
    return pd.read_csv(path_file_csv)


@pytest.fixture
def dataframe_kidney_clean() -> pd.DataFrame:
    """
    Fixture for loading a dataframe with no missing values

    :return: dataframe_kidney_clean: A dataframe with no missing fields
    :rtype: class : pd.DataFrame
    """

    path_file_csv = os.path.join(DATA_PATH, "data_csv_kidney_clean", "kidney_disease_clean.csv")
    return pd.read_csv(path_file_csv)


@pytest.fixture
def dataframe_kidney_clean_remote(
    dataframe_kidney_clean,
    connect_to_one_VM,
):
    """
    Fixture for creating a remote data frame with cleaned kidney data

    :param dataframe_kidney_clean: raw dataframe
    :type dataframe_kidney_clean: pd.DataFrame
    :param connect_to_one_VM: the clients object
    :type connect_to_one_VM: zero.ZeroClient
    :return: remote dataframe
    :rtype: zero.DataFrameRemote
    """
    client = connect_to_one_VM
    df = dataframe_kidney_clean
    return client.proxy("DataFrameRemote", serializer_table[str(type(df))](df))


@pytest.fixture
def scheme_kidney() -> dict:
    """
    Fixture for loading the scheme for kidney dataset

    :return: scheme_kidney: Scheme is associated with the kidney dataset
    :rtype: class : dict
    """

    path_file_json = os.path.join(DATA_PATH, "data_csv_kidney_clean", "schema.json")
    file = open(path_file_json, "r")
    schema_content = file.read()
    return json.loads(schema_content)


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

    sample_0 = [client.proxy("SeriesRemote", sample_0_numpy)]
    sample_1 = [client.proxy("SeriesRemote", sample_1_numpy)]
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

    sample_0 = [client.proxy("SeriesRemote", sample_0_numpy)]
    sample_1 = [client.proxy("SeriesRemote", sample_1_numpy)]
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

    sample_0 = [client.proxy("SeriesRemote", sample_0_numpy)]
    sample_1 = [client.proxy("SeriesRemote", sample_1_numpy)]
    return (sample_0, sample_1)


@pytest.fixture
def one_sample_normal_remote(
    connect_to_one_VM,
) -> List:
    """
    Fixture for creating a remote dataframe with raw numpy data follows normal distribution

    :param connect_to_one_VM: client object
    :type connect_to_one_VM: zero.ZeroClient
    :return: The remote dataframe
    :rtype: List
    """
    client = connect_to_one_VM

    sample_0_numpy = utils.random_normal(client, 0, 1, 17, 42)

    sample_0 = [client.proxy("SeriesRemote", sample_0_numpy)]
    return sample_0


@pytest.fixture
def two_sample_normal_remote(
    connect_to_one_VM,
) -> List:
    """
    Fixture for creating two remote dataframe following normal distribution

    :param connect_to_one_VM: client objects
    :type connect_to_one_VM: zero.ZeroClient
    :return: the remote dataframe
    :rtype: List
    """
    client = connect_to_one_VM

    sample_0_numpy = utils.random_normal(client, 0, 1, 2000, 42)
    sample_1_numpy = utils.random_normal(client, 0, 1, 2000, 24)

    return ([client.proxy("SeriesRemote", sample_0_numpy)], [client.proxy("SeriesRemote", sample_1_numpy)])


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
def one_sample_normal_local() -> np.ndarray:
    """
    Fixture for creating a local normal sample

    :return: array with normal distribution
    :rtype: np.ndarray
    """

    np.random.seed(42)
    array_sample_0 = np.random.normal(0, 1, 17)  # works from size 17 onwards

    return array_sample_0


@pytest.fixture
def two_sample_normal_local() -> Tuple:
    """
    Fixture for creating two sample following normal distribution

    :return: two sample with normal distribution
    :rtype: Tuple
    """

    np.random.seed(42)
    array_sample_0 = np.random.normal(0, 1, 2000)
    array_sample_1 = np.random.normal(0, 1, 2000)

    return (array_sample_0, array_sample_1)


@pytest.fixture
def get_basic_linear_dataframe():
    """
    To be used by test function. This generates a dataframe containing two linear functions to be learned
    :return: A Dataframe containing points belonging to two linear functions
    :type: pd.DataFrame
    """

    x_values = [i for i in range(100)]
    x_train = np.array(x_values, dtype=np.float32)
    x_train = x_train.reshape(-1, 1)

    y_values_1 = [2 * i + 1 for i in x_values]
    y_train_1 = np.array(y_values_1, dtype=np.float32)
    y_train_1 = y_train_1.reshape(-1, 1)

    df_X = pd.DataFrame(x_train, columns=["X"])
    df_Y1 = pd.DataFrame(y_train_1, columns=["Y"])

    df = pd.concat([df_X, df_Y1], axis=1)
    return df


@pytest.fixture
def get_linear_federation_split(
    get_basic_linear_dataframe,
    connect_to_three_VMs,
):
    """
    Fixture for getting a federated dataset with the linear dataframe

    :param get_basic_linear_dataframe: a dataframe containing linear X-Y pair
    :type get_basic_linear_dataframe: pd.Dataframe
    :param connect_to_three_VMs: Client objects
    :type connect_to_three_VMs: zero.ZeroClient
    :return: The train(remote) and test set(local)
    :rtype: tuple
    """
    NUMBER_PARTICIPANTS = 3
    TEST_SAMPLE = 0.8
    df = get_basic_linear_dataframe
    clients = connect_to_three_VMs

    train = df.sample(frac=TEST_SAMPLE, random_state=0)
    test = df.drop(train.index)

    shuffled = train.sample(frac=1)
    result = np.array_split(shuffled, NUMBER_PARTICIPANTS)

    train_set = []
    for i in range(3):

        train_data = clients[i].proxy("DataFrameRemote", serializer_table[str(type(result[i]))](result[i]))
        train_set.append(train_data)

    return train_set, test


@pytest.fixture
def get_kidney_federation_split(
    dataframe_kidney_clean,
    connect_to_three_VMs,
):
    """
    fixture for creating a federation set with kidney data

    :param dataframe_kidney_clean: cleaned kidney dataframe
    :type dataframe_kidney_clean: pd.DataFrame
    :param connect_to_three_VMs: client objects
    :type connect_to_three_VMs: zero.ZeroClients
    :return: train(remote) and test(local) sets
    :rtype: tuple
    """
    clients = connect_to_three_VMs
    NUMBER_PARTICIPANTS = 3
    TEST_SAMPLE = 0.8

    df = pd.get_dummies(data=dataframe_kidney_clean)
    clients = connect_to_three_VMs

    train = df.sample(frac=TEST_SAMPLE, random_state=0)
    test = df.drop(train.index)

    shuffled = train.sample(frac=1)
    result = np.array_split(shuffled, NUMBER_PARTICIPANTS)

    train_set = []
    for i in range(3):
        train_data = clients[i].proxy("DataFrameRemote", serializer_table[str(type(result[i]))](result[i]))
        train_set.append(train_data)

    return train_set, test


@pytest.fixture
def get_iris_dataframe():
    """
    To be used by test function. This pulls a copy of the iris dataset and creates a Dataframe containing a one hot encoded version of it.
    :return: A one hot encded Dataframe containing points belonging to the iris dataset
    :type: pd.DataFrame
    """

    iris = load_iris()
    df1 = pd.DataFrame(iris.data, columns=iris.feature_names)
    target = iris.target_names
    encoder = OneHotEncoder(sparse=False)
    target = encoder.fit_transform(iris.target.reshape(-1, 1))
    df2 = pd.get_dummies(pd.DataFrame(target, columns=iris.target_names))
    dataframe = pd.concat([df1, df2], axis=1)

    return dataframe


@pytest.fixture
def get_iris_federation_split(
    connect_to_three_VMs,
    get_iris_dataframe,
):
    """
    To be used by test function. This runs the federated averaging on a basic linear function and returns the r2 score of the trained model.
    :param: df: dataframe to be split into federated participants
    :type df: pd.DataFrame
    :return result: A list of dataframes containing a representation of the data federation
    :type result: List[pd.DataFrame]
    :return test: A sample from the original Dataframe which will be used for testing
    :type test: pd.DataFrame
    """

    NUMBER_PARTICIPANTS = 3
    TEST_SAMPLE = 0.8
    df = get_iris_dataframe
    clients = connect_to_three_VMs

    train = df.sample(frac=TEST_SAMPLE, random_state=0)
    test = df.drop(train.index)

    shuffled = train.sample(frac=1)
    result = np.array_split(shuffled, NUMBER_PARTICIPANTS)

    train_set = []
    for i in range(3):
        train_data = clients[i].proxy("DataFrameRemote", serializer_table[str(type(result[i]))](result[i]))
        train_set.append(train_data)

    return train_set, test
