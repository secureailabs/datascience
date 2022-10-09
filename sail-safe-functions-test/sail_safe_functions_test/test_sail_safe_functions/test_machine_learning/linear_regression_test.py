import numpy as np
import pytest
import torch
from sail_safe_functions_orchestrator.machine_learning import LinearRegression, federated_averaging
from sklearn.metrics import r2_score


def predict_basic_linear(clients, epochs, federal_epochs, data_federation, test):
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
    model_type = "linear_regression"
    learn_rate = 0.0001

    model = federated_averaging(
        clients,
        epochs,
        federal_epochs,
        data_federation,
        X_col,
        Y_col,
        learn_rate,
        starting_model,
        model_type,
        criterion,
        optimizer,
    )

    predicted = model(torch.Tensor(test[X_col].values).float()).detach()
    Y_test = torch.Tensor(test[Y_col].values).float()

    return r2_score(predicted, Y_test)


def predict_basic_kidney(clients, epochs, federal_epochs, data_federation, test):
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
    model_type = "linear_regression"
    learn_rate = 0.0001

    model = federated_averaging(
        clients,
        epochs,
        federal_epochs,
        data_federation,
        X_col,
        Y_col,
        learn_rate,
        starting_model,
        model_type,
        criterion,
        optimizer,
    )

    predicted = model(torch.Tensor(test[X_col].values).float()).detach()
    Y_test = torch.Tensor(test[Y_col].values).float()

    return r2_score(predicted, Y_test)


@pytest.mark.active
def test_basic_linear_data_acceptable(
    connect_to_three_VMs,
    get_linear_federation_split,
):
    """
    This tests whether the model is learning basic linear functions. The R2 score is evaluated
    to see whether it meets a a threshold of 0.95 in order to pass this test.
    """

    # Arrange
    random_seed = 1
    torch.manual_seed(random_seed)
    np.random.seed(random_seed)

    data_federation, test = get_linear_federation_split
    clients = connect_to_three_VMs

    # Action
    R2 = predict_basic_linear(
        clients,
        epochs=100,
        federal_epochs=5,
        data_federation=data_federation,
        test=test,
    )

    # Assert scores are acceptable
    assert R2 >= 0.95

    # TODO: Produce plot of accuracy improvement over federal epochs


@pytest.mark.active
def test_linear_kidney_data_acceptable(
    connect_to_three_VMs,
    get_kidney_federation_split,
):
    """
    This tests whether the model is learning some sample data from the kidney dataset. The R2 score is evaluated
    to see whether it meets a a threshold of 0.95 in order to pass this test.
    TODO: currently a suitable set of inputs was not found to predict the kidny data well. For now X and Y are clones of each other
    """
    # Arrange
    random_seed = 1
    torch.manual_seed(random_seed)
    np.random.seed(random_seed)

    data_federation, test = get_kidney_federation_split
    clients = connect_to_three_VMs

    # Action
    R2 = predict_basic_kidney(
        clients,
        epochs=15,
        federal_epochs=5,
        data_federation=data_federation,
        test=test,
    )

    # Assert scores are acceptable
    assert R2 >= 0.95

    # TODO: Produce plot of accuracy improvement over federal epochs
