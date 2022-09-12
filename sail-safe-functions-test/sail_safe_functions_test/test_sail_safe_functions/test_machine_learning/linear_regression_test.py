import pytest
from sail_safe_functions_orchestrator.data_frame_federated import DataFrameFederated

from sail_safe_functions_orchestrator.machine_learning.federated_averaging import (
    federated_averaging,
)
from helper_libs.shared.models.LinearRegression import LinearRegression

import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from sklearn.datasets import load_iris
from sklearn.metrics import r2_score
import torch
import numpy as np


import random


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


def get_test_federation_split(df):
    """
    To be used by test function. This runs the federated averaging on a basic linear function and returns the r2 score of the trained model.

    :param: df: dataframe to be split into federated participants
    :type df: pd.DataFrame
    :return result: A list of dataframes containing a representation of the data federation
    :type result: List[pd.DataFrame]
    :return test: A sample from the original Dataframe which will be used for testing
    :type test: pd.DataFrame
    """

    NUMBER_PARTICIPANTS = 5
    TEST_SAMPLE = 0.8

    train = df.sample(frac=TEST_SAMPLE, random_state=0)
    test = df.drop(train.index)

    shuffled = train.sample(frac=1)
    result = np.array_split(shuffled, NUMBER_PARTICIPANTS)

    return result, test


def predict_basic_linear(epochs, federal_epochs, data_federation, test):
    """
    To be used by test function. This runs the federated averaging on a basic linear function and returns the r2 score of the trained model.

    :param epochs: The number of epochs each federated member will run for
    :type: epochs: Integer
    :param federal_epochs: The number of model averaging rounds the test will run for
    :type: federal_epochs: Integer
    :param: data_federation: A list of dataframes containing the data of each participant
    :type: data_federation: List[pd.DataFrame]
    :param: test: Test data to be used to validate the model
    :type: pd.DataFrame
    :return: The R2 score of the model that was trained
    :type: Float
    """
    X_col = ["X"]
    Y_col = ["Y"]
    in_layer = len(X_col)
    out_layer = len(Y_col)
    optimizer = "SGD"
    criterion = "MSELoss"
    starting_model = LinearRegression(in_layer, out_layer)
    learn_rate = 0.0001

    model = federated_averaging(
        epochs,
        federal_epochs,
        data_federation,
        X_col,
        Y_col,
        learn_rate,
        starting_model,
        criterion,
        optimizer,
    )

    predicted = model(torch.Tensor(test[X_col].values).float()).detach()
    Y_test = torch.Tensor(test[Y_col].values).float()

    return r2_score(predicted, Y_test)


def predict_basic_kidney(epochs, federal_epochs, data_federation, test):
    """
    To be used by test function. This runs federated averaging on kidney and returns the r2 score of the trained model.
        TODO: This is currently using X and Y as the same column as nothing suitable was found in kidney data for learning for now.

    :param epochs: The number of epochs each federated member will run for
    :type: epochs: Integer
    :param federal_epochs: The number of model averaging rounds the test will run for
    :type: federal_epochs: Integer
    :param: data_federation: A list of dataframes containing the data of each participant
    :type: data_federation: List[pd.DataFrame]
    :param: test: Test data to be used to validate the model
    :type: pd.DataFrame
    :return: The R2 score of the model that was trained
    :type: Float
    """
    X_col = ["age"]
    Y_col = ["age"]
    in_layer = len(X_col)
    out_layer = len(Y_col)
    optimizer = "SGD"
    criterion = "MSELoss"
    starting_model = LinearRegression(in_layer, out_layer)
    learn_rate = 0.0001

    model = federated_averaging(
        epochs,
        federal_epochs,
        data_federation,
        X_col,
        Y_col,
        learn_rate,
        starting_model,
        criterion,
        optimizer,
    )

    predicted = model(torch.Tensor(test[X_col].values).float()).detach()
    Y_test = torch.Tensor(test[Y_col].values).float()

    return r2_score(predicted, Y_test)


@pytest.mark.active
def test_basic_linear_data_acceptable():
    """
    This tests whether the model is learning basic linear functions. The R2 score is evaluated
    to see whether it meets a a threshold of 0.95 in order to pass this test.
    """

    # Arrange
    random_seed = 1
    torch.manual_seed(random_seed)
    torch.cuda.manual_seed(random_seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False
    np.random.seed(random_seed)

    dataframe = get_basic_linear_dataframe()
    data_federation, test = get_test_federation_split(dataframe)

    # Action
    R2 = predict_basic_linear(
        epochs=100,
        federal_epochs=5,
        data_federation=data_federation,
        test=test,
    )

    # Assert scores are acceptable
    assert R2 >= 0.95

    # TODO: Produce plot of accuracy improvement over federal epochs


@pytest.mark.active
def test_linear_kidney_data_acceptable(dataframe_kidney_clean: pd.DataFrame):
    """
    This tests whether the model is learning some sample data from the kidney dataset. The R2 score is evaluated
    to see whether it meets a a threshold of 0.95 in order to pass this test.
    TODO: currently a suitable set of inputs was not found to predict the kidny data well. For now X and Y are clones of each other
    """
    # Arrange
    random_seed = 1
    torch.manual_seed(random_seed)
    torch.cuda.manual_seed(random_seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False
    np.random.seed(random_seed)

    dataframe = pd.get_dummies(data=dataframe_kidney_clean)
    data_federation, test = get_test_federation_split(dataframe)

    # Action
    R2 = predict_basic_kidney(
        epochs=15,
        federal_epochs=5,
        data_federation=data_federation,
        test=test,
    )

    # Assert scores are acceptable
    assert R2 >= 0.95

    # TODO: Produce plot of accuracy improvement over federal epochs
