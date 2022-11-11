"""
Pytest fixtures
"""
import json
import os
from typing import Tuple

import numpy as np
import pandas as pd
import pytest
from config import DATA_PATH
from sail_safe_functions_orchestrator.data_frame_federated import DataFrameFederated
from sail_safe_functions_orchestrator.dataset_longitudinal_federated import DatasetLongitudinalFederated
from sail_safe_functions_orchestrator.series_federated import SeriesFederated
from sail_safe_functions_test.helper_sail_safe_functions.data_frame_federated_local import DataFrameFederatedLocal
from sail_safe_functions_test.helper_sail_safe_functions.series_federated_local import SeriesFederatedLocal


@pytest.fixture
def dataset_longitudinal_r4sep2019_20_1() -> DatasetLongitudinalFederated:
    path_file_data_federation = os.path.join(DATA_PATH, "data_federation_packaged", "r4sep2019_fhirv1_20_1.zip")
    return DatasetLongitudinalFederated.read_for_path_file(path_file_data_federation)


@pytest.fixture
def dataset_longitudinal_r4sep2019_1k_3() -> DatasetLongitudinalFederated:
    path_file_data_federation = os.path.join(DATA_PATH, "data_federation_packaged", "r4sep2019_fhirv1_1k_3.zip")
    return DatasetLongitudinalFederated.read_for_path_file(path_file_data_federation)


@pytest.fixture
def data_frame_federated_kidney() -> DataFrameFederated:
    """
    Fixture for loading a dataframe with missing values
    :return: data_frame_federated_kidney: a federated dataframe
    :rtype: class : DataFrameFederatedLocal
    """

    list_name_file_csv = ["kidney_disease_clean.csv"]
    id_column_0 = "PD-L1 level before treatment"

    dict_csv = {}
    for name_file_csv in list_name_file_csv:
        path_file_csv = os.path.join(DATA_PATH, "data_csv_kidney_clean", name_file_csv)
        dict_csv[name_file_csv] = path_file_csv
    return DataFrameFederatedLocal.from_csv(dict_csv)


@pytest.fixture
def data_frame_federated_kidney_hasnan() -> DataFrameFederated:
    """
    Fixture for loading a dataframe with missing values
    :return: data_frame_federated_kidney: a federated dataframe
    :rtype: class : DataFrameFederatedLocal
    """

    list_name_file_csv = ["kidney_disease.csv"]
    id_column_0 = "PD-L1 level before treatment"

    dict_csv = {}
    for name_file_csv in list_name_file_csv:
        path_file_csv = os.path.join(DATA_PATH, "data_csv_kidney", name_file_csv)
        dict_csv[name_file_csv] = path_file_csv
    return DataFrameFederatedLocal.from_csv(dict_csv)


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
def one_sample_big() -> SeriesFederatedLocal:
    """
    Fixture for SeriesFederatedLocal with this first part of the investor demo dataset

    :return: DataFrameFederatedLocal
    :rtype: class : test_sail_safe_functions.series_federated_local.SeriesFederatedLocal
    """
    list_name_file_csv = ["bmc1.csv", "bwh1.csv", "mgh1.csv"]
    id_column_0 = "PD-L1 level before treatment"

    dict_csv = {}
    for name_file_csv in list_name_file_csv:
        path_file_csv = os.path.join(DATA_PATH, "data_csv_investor_demo", name_file_csv)
        dict_csv[name_file_csv] = path_file_csv
    data_frame_federated = DataFrameFederatedLocal.from_csv(dict_csv)
    return data_frame_federated[id_column_0]


@pytest.fixture
def two_sample_big() -> SeriesFederatedLocal:
    """
    Fixture for SeriesFederatedLocal with this first part of the investor demo dataset

    :return: DataFrameFederatedLocal
    :rtype: class : test_sail_safe_functions.series_federated_local.SeriesFederatedLocal
    """
    list_name_file_csv = ["bmc1.csv", "bwh1.csv", "mgh1.csv"]
    id_column_0 = "PD-L1 level before treatment"
    id_column_1 = "PD-L1 level after treatment"

    dict_csv = {}
    for name_file_csv in list_name_file_csv:
        path_file_csv = os.path.join(DATA_PATH, "data_csv_investor_demo", name_file_csv)
        dict_csv[name_file_csv] = path_file_csv
    data_frame = DataFrameFederatedLocal.from_csv(dict_csv)

    return (data_frame[id_column_0], data_frame[id_column_1])


@pytest.fixture
def two_sample_categorical() -> SeriesFederatedLocal:
    """
    Fixture for SeriesFederatedLocal with this first part of the kidney disease dataset

    :return: DataFrameFederatedLocal
    :rtype: class : test_sail_safe_functions.series_federated_local.SeriesFederatedLocal
    """
    list_name_file_csv = ["kidney_disease_clean.csv"]
    id_column_0 = "rbc"
    id_column_1 = "classification"

    dict_csv = {}
    for name_file_csv in list_name_file_csv:
        path_file_csv = os.path.join(DATA_PATH, "data_csv_kidney_clean", name_file_csv)
        dict_csv[name_file_csv] = path_file_csv
    data_frame = DataFrameFederatedLocal.from_csv(dict_csv)

    return (data_frame[id_column_0], data_frame[id_column_1])


@pytest.fixture
def two_sample_small() -> Tuple[SeriesFederatedLocal, SeriesFederatedLocal]:
    """
    A two sample tuple with data from wikipedia

    :return: SeriesFederatedLocal
    :rtype: class : test_sail_safe_functions.series_federated_local.SeriesFederatedLocal
    """
    sample_0_numpy = np.array([17.2, 20.9, 22.6, 18.1, 21.7, 21.4, 23.5, 24.2, 14.7, 21.8])
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

    sample_0 = SeriesFederatedLocal.from_array("dataset_0", "sample_0", sample_0_numpy)
    sample_1 = SeriesFederatedLocal.from_array("dataset_0", "sample_1", sample_1_numpy)
    return (sample_0, sample_1)


@pytest.fixture
def two_sample_small_two() -> Tuple[SeriesFederatedLocal, SeriesFederatedLocal]:
    """
    A two sample tuple with data from wikipedia

    :return: SeriesFederatedLocal
    :rtype: class : test_sail_safe_functions.series_federated_local.SeriesFederatedLocal
    """
    sample_0_numpy = np.array([14, 34, 16, 43, 45, 36, 42, 43, 16, 27])
    sample_1_numpy = np.array([34, 36, 44, 18, 42, 39, 16, 35, 15, 33])

    sample_0 = SeriesFederatedLocal.from_array("dataset_0", "sample_0", sample_0_numpy)
    sample_1 = SeriesFederatedLocal.from_array("dataset_0", "sample_1", sample_1_numpy)
    return (sample_0, sample_1)


@pytest.fixture
def two_sample_small_paired() -> Tuple[SeriesFederated, SeriesFederated]:
    """
    A two sample tuple with data from https://en.wikipedia.org/wiki/Student%27s_t-test#Dependent_t-test_for_paired_samples

    :return: SeriesFederatedLocal
    :rtype: class : test_sail_safe_functions.series_federated_local.SeriesFederatedLocal
    """
    sample_0_numpy = np.array([30.02, 29.99, 30.11, 29.97, 30.01, 29.99])
    sample_1_numpy = np.array([29.89, 29.93, 29.72, 29.98, 30.02, 29.98])

    sample_0 = SeriesFederatedLocal.from_array("dataset_0", "sample_0", sample_0_numpy)
    sample_1 = SeriesFederatedLocal.from_array("dataset_0", "sample_1", sample_1_numpy)

    return (sample_0, sample_1)
