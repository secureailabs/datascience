"""
Pytest fixtures
"""
import json
import os
from typing import Tuple

import numpy as np
import pytest
from sail_core.implementation_manager import ImplementationManager
from sail_safe_functions.aggregator.data_frame_federated import DataFrameFederated
from sail_safe_functions.aggregator.dataset_longitudinal_federated import DatasetLongitudinalFederated
from sail_safe_functions.aggregator.series_federated import SeriesFederated
from sail_safe_functions.test.config import DATA_PATH
from sail_safe_functions.test.helper_sail_safe_functions.participant_service_local import ParticipantSeriviceLocal
from sail_safe_functions.test.helper_sail_safe_functions.tools_data_test import ToolsDataTest


def pytest_sessionstart(session):
    """
    Called after the Session object has been created and
    before performing collection and entering the run test loop.
    """
    implementation_manager = ImplementationManager.get_instance()
    implementation_manager.set_participant_service(ParticipantSeriviceLocal())
    implementation_manager.initialize()


def pytest_sessionfinish(session, exitstatus):
    """
    Called after whole test run finished, right before
    returning the exit status to the system.
    """


@pytest.fixture
def dataset_longitudinal_r4sep2019_20_1() -> DatasetLongitudinalFederated:
    path_file_data_federation = os.path.join(DATA_PATH, "data_federation_packaged", "r4sep2019_fhirv1_20_1.zip")
    return ToolsDataTest.read_for_path_file(path_file_data_federation)


@pytest.fixture
def dataset_longitudinal_r4sep2019_1k_3() -> DatasetLongitudinalFederated:
    path_file_data_federation = os.path.join(DATA_PATH, "data_federation_packaged", "r4sep2019_fhirv1_1k_3.zip")
    return ToolsDataTest.read_for_path_file(path_file_data_federation)


@pytest.fixture
def data_frame_federated_kidney() -> DataFrameFederated:
    """
    Fixture for loading a dataframe with missing values
    :return: data_frame_federated_kidney: a federated dataframe
    :rtype: class : DataFrameFederatedLocal
    """

    return load_kidney_clean(DATA_PATH)


def load_kidney_clean(data_path: str) -> DataFrameFederated:
    list_name_file_csv = ["kidney_disease_clean.csv"]
    dict_csv = {}
    for name_file_csv in list_name_file_csv:
        path_file_csv = os.path.join(data_path, "data_csv_kidney_clean", name_file_csv)
        dict_csv[name_file_csv] = path_file_csv
    return ToolsDataTest.from_csv(dict_csv)


@pytest.fixture
def data_frame_federated_kidney_hasnan() -> DataFrameFederated:
    """
    Fixture for loading a dataframe with missing values
    :return: data_frame_federated_kidney: a federated dataframe
    :rtype: class : DataFrameFederated
    """

    return load_kidney_hasnan(DATA_PATH)


def load_kidney_hasnan(data_path: str) -> DataFrameFederated:
    list_name_file_csv = ["kidney_disease.csv"]
    dict_csv = {}
    for name_file_csv in list_name_file_csv:
        path_file_csv = os.path.join(data_path, "data_csv_kidney", name_file_csv)
        dict_csv[name_file_csv] = path_file_csv
    return ToolsDataTest.from_csv(dict_csv)


@pytest.fixture
def one_sample_big() -> SeriesFederated:
    """
    Fixture for SeriesFederated with this first part of the investor demo dataset
    """
    id_column_0 = "PD-L1 level before treatment"
    data_frame = load_investor(DATA_PATH)
    return data_frame[id_column_0]


@pytest.fixture
def two_sample_big() -> Tuple[SeriesFederated, SeriesFederated]:
    """
    Fixture for SeriesFederated with this first part of the investor demo dataset
    """
    id_column_0 = "PD-L1 level before treatment"
    id_column_1 = "PD-L1 level after treatment"
    data_frame = load_investor(DATA_PATH)

    return (data_frame[id_column_0], data_frame[id_column_1])


def load_investor(data_path: str) -> DataFrameFederated:
    list_name_file_csv = ["bmc1.csv", "bwh1.csv", "mgh1.csv"]

    dict_csv = {}
    for name_file_csv in list_name_file_csv:
        path_file_csv = os.path.join(data_path, "data_csv_investor_demo", name_file_csv)
        dict_csv[name_file_csv] = path_file_csv
    return ToolsDataTest.from_csv(dict_csv)


@pytest.fixture
def two_sample_categorical() -> Tuple[SeriesFederated, SeriesFederated]:
    """
    Fixture for a tuple of two SeriesFederated with this first part of the kidney disease dataset
    """
    id_column_0 = "rbc"
    id_column_1 = "classification"
    data_frame = load_kidney_clean(DATA_PATH)
    return (data_frame[id_column_0], data_frame[id_column_1])


@pytest.fixture
def two_sample_small() -> Tuple[SeriesFederated, SeriesFederated]:
    """
    A two sample tuple with data from wikipedia
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

    sample_0 = ToolsDataTest.from_array("dataset_0", "sample_0", sample_0_numpy)
    sample_1 = ToolsDataTest.from_array("dataset_0", "sample_1", sample_1_numpy)
    return (sample_0, sample_1)


@pytest.fixture
def two_sample_small_two() -> Tuple[SeriesFederated, SeriesFederated]:
    """
    A two sample tuple with data from wikipedia
    """
    sample_0_numpy = np.array([14, 34, 16, 43, 45, 36, 42, 43, 16, 27])
    sample_1_numpy = np.array([34, 36, 44, 18, 42, 39, 16, 35, 15, 33])

    sample_0 = ToolsDataTest.from_array("dataset_0", "sample_0", sample_0_numpy)
    sample_1 = ToolsDataTest.from_array("dataset_0", "sample_1", sample_1_numpy)
    return (sample_0, sample_1)


@pytest.fixture
def two_sample_small_paired() -> Tuple[SeriesFederated, SeriesFederated]:
    """
    A two sample tuple with data from https://en.wikipedia.org/wiki/Student%27s_t-test#Dependent_t-test_for_paired_samples
    """
    sample_0_numpy = np.array([30.02, 29.99, 30.11, 29.97, 30.01, 29.99])
    sample_1_numpy = np.array([29.89, 29.93, 29.72, 29.98, 30.02, 29.98])

    sample_0 = ToolsDataTest.from_array("dataset_0", "sample_0", sample_0_numpy)
    sample_1 = ToolsDataTest.from_array("dataset_0", "sample_1", sample_1_numpy)

    return (sample_0, sample_1)


@pytest.fixture
def data_frame_federated_house() -> DataFrameFederated:
    """
    Fixture for loading a dataframe with missing values
    :return: data_frame_federated_kidney: a federated dataframe
    :rtype: class : DataFrameFederatedLocal
    """

    return load_house(DATA_PATH)


def load_house(data_path: str) -> DataFrameFederated:
    list_name_file_csv = ["california_housing_train.csv"]

    dict_csv = {}
    for name_file_csv in list_name_file_csv:
        path_file_csv = os.path.join(data_path, "data_csv_house", name_file_csv)
        dict_csv[name_file_csv] = path_file_csv
    return ToolsDataTest.from_csv(dict_csv)


@pytest.fixture
def data_frame_federated_cardio() -> DataFrameFederated:
    """
    Fixture for loading a dataframe with missing values
    :return: data_frame_federated_kidney: a federated dataframe
    :rtype: class : DataFrameFederatedLocal
    """
    return load_cardio(DATA_PATH)


def load_cardio(data_path: str) -> DataFrameFederated:
    list_name_file_csv = ["cardio_70000_0.csv", "cardio_70000_1.csv", "cardio_70000_2.csv"]
    dict_csv = {}
    for name_file_csv in list_name_file_csv:
        path_file_csv = os.path.join(data_path, "data_csv_cardio", name_file_csv)
        dict_csv[name_file_csv] = path_file_csv
    return ToolsDataTest.from_csv(dict_csv)


@pytest.fixture
def data_frame_federated_gdc_941_1() -> DataFrameFederated:
    """
    Fixture for loading a dataframe with missing values
    :return: data_frame_federated_kidney: a federated dataframe
    :rtype: class : DataFrameFederatedLocal
    """
    return load_gdc_941_1(DATA_PATH)


def load_gdc_941_1(data_path: str) -> DataFrameFederated:
    list_name_file_csv = ["gdc_csvv1_941_0.csv"]
    dict_csv = {}
    for name_file_csv in list_name_file_csv:
        path_file_csv = os.path.join(data_path, "data_csv_gdc_941_1", name_file_csv)
        dict_csv[name_file_csv] = path_file_csv
    return ToolsDataTest.from_csv(dict_csv)
