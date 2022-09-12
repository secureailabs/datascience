import pytest
from sail_safe_functions_orchestrator.data_frame_federated import DataFrameFederated

from sail_safe_functions_orchestrator.machine_learning.federated_averaging import (
    federated_averaging,
)
from helper_libs.shared.models.LogisticRegression import LogisticRegression

import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from sklearn.datasets import load_iris
from sklearn.metrics import precision_score, recall_score, f1_score
import torch
import numpy as np

import random


def get_iris_dataframe():
    """To be used by test function. This pulls a copy of the iris dataset and creates a Dataframe containing a one hot encoded version of it.

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


def get_test_federation_split(df):
    """To be used by test function. This runs the federated averaging on a basic linear function and returns the r2 score of the trained model.

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


def score_model(predicted, Y_test):
    """Evaluates a set of predictions vs their actual labels.

    :param: predicted: a list of precitions in one-hot encoding
    :type: predicted: Torch.Tensor
    :param Y_test: The List of labels
    :type: Y_test: Torch.Tensor
    :return: precision: The precision metric
    :type: precision: float
    :return recall: The recall metric
    :type: recall: float
    :return: f1: The f1 score of the predictions
    :type: f1: float
    """
    predictions = []
    for prediction in predicted:
        predictions.append(prediction.argmax())

    labels = []
    for y in Y_test:
        labels.append(int(y.argmax()))

    precision = precision_score(predictions, labels, average="weighted")
    recall = recall_score(predictions, labels, average="weighted")
    f1 = f1_score(predictions, labels, average="weighted")

    return precision, recall, f1


def predict_iris(epochs, federal_epochs, data_federation, test):
    """To be used by test function. Runs federated averaging on iris data and returns metrics of trained model.

    :param epochs: The number of epochs each federated member will run for
    :type: epochs: Integer
    :param federal_epochs: The number of model averaging rounds the test will run for
    :type: federal_epochs: Integer
    :param: data_federation: A list of dataframes containing the data of each participant
    :type: data_federation: List[pd.DataFrame]
    :param: test: Test data to be used to validate the model
    :type: pd.DataFrame
    :return: precision: The precision metric
    :type: precision: float
    :return recall: The recall metric
    :type: recall: float
    :return: f1: The f1 score of the predictions
    :type: f1: float
    """
    X_col = [
        "sepal length (cm)",
        "sepal width (cm)",
        "petal length (cm)",
        "petal width (cm)",
    ]
    Y_col = ["setosa", "versicolor", "virginica"]
    in_layer = len(X_col)
    out_layer = len(Y_col)
    optimizer = "SGD"
    criterion = "MSELoss"
    starting_model = LogisticRegression(in_layer, out_layer)
    learn_rate = 0.1
    epochs = 500
    federal_epochs = 5

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

    predicted = model(torch.Tensor(test[X_col].values).float())
    Y_test = torch.Tensor(test[Y_col].values).float()

    return score_model(predicted, Y_test)


def predict_kidney(epochs, federal_epochs, data_federation, test):
    """To be used by test function. Runs federated averaging on kidney data and returns metrics of trained model.

    :param epochs: The number of epochs each federated member will run for
    :type: epochs: Integer
    :param federal_epochs: The number of model averaging rounds the test will run for
    :type: federal_epochs: Integer
    :param: data_federation: A list of dataframes containing the data of each participant
    :type: data_federation: List[Dataframe]
    :param: test: Test data to be used to validate the model
    :type: DataFrame
    :return: precision: The precision metric
    :type: precision: float
    :return recall: The recall metric
    :type: recall: float
    :return: f1: The f1 score of the predictions
    :type: f1: float
    """

    X_col = ["age", "bp", "sg", "al"]
    Y_col = ["classification_ckd"]
    in_layer = len(X_col)
    out_layer = len(Y_col)
    optimizer = "SGD"
    criterion = "BCELoss"
    starting_model = LogisticRegression(in_layer, out_layer)
    learn_rate = 0.001

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

    X_test = torch.Tensor(test[X_col].values).float()
    Y_test = torch.Tensor(test[Y_col].values).float()
    predicted = model(X_test).detach()

    predictions = []
    for prediction in predicted:
        if prediction > 0.5:
            predictions.append(1)
        else:
            predictions.append(0)

    precision = precision_score(predictions, Y_test, average="weighted")
    recall = recall_score(predictions, Y_test, average="weighted")
    f1 = f1_score(predictions, Y_test, average="weighted")

    return precision, recall, f1


@pytest.mark.active
def test_kidney_data_acceptable(dataframe_kidney_clean: pd.DataFrame):
    """This tests whether the model is learning on the real kidney data. The precision, recall and f1 score is evaluated
    to see whether it meets a a threshold in order to pass this test.

    :param:  dataframe_kidney_clean: Dataframe containing kidney data
    :type: dataframe_kidney_clean:: pd.DataFrame
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
    precision_1000_4, recall_1000_4, f1_1000_4 = predict_kidney(
        epochs=5000,
        federal_epochs=4,
        data_federation=data_federation,
        test=test,
    )
    # precision_1000_1, recall_1000_1, f1_1000_1 = predict_kidney(
    #     epochs=5000,
    #     federal_epochs=1,
    #     data_federation=data_federation,
    #     test=test,
    # )

    # Assert scores are acceptable
    assert precision_1000_4 >= 0.7
    assert recall_1000_4 >= 0.7
    assert f1_1000_4 >= 0.7

    # Assert scores are better after multiple rounds of averaging
    # assert precision_1000_4 >= precision_1000_1
    # assert recall_1000_4 >= recall_1000_1
    # assert f1_1000_4 >= f1_1000_1


@pytest.mark.active
def test_iris_data_acceptable():
    # Arrange
    random_seed = 1
    torch.manual_seed(random_seed)
    torch.cuda.manual_seed(random_seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False
    np.random.seed(random_seed)

    dataframe = get_iris_dataframe()
    data_federation, test = get_test_federation_split(dataframe)

    # Action
    precision_1000_5, recall_1000_5, f1_1000_5 = predict_iris(
        epochs=500,
        federal_epochs=5,
        data_federation=data_federation,
        test=test,
    )
    precision_1000_1, recall_1000_1, f1_1000_1 = predict_iris(
        epochs=500,
        federal_epochs=1,
        data_federation=data_federation,
        test=test,
    )

    # Assert scores are acceptable
    assert precision_1000_5 >= 0.6
    assert recall_1000_5 >= 0.6
    assert f1_1000_5 >= 0.6

    # Assert scores are better after multiple rounds of averaging
    # assert precision_1000_5 >= precision_1000_1
    # assert recall_1000_5 >= recall_1000_1
    # assert f1_1000_5 >= f1_1000_1

    # TODO: Produce plot of accuracy improvement over federal epochs
