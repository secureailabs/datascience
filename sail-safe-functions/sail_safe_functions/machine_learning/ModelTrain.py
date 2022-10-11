from tokenize import String
from typing import Type

import torch
from sail_safe_functions.machine_learning.ModelUtility import ModelUtility, load_model_dict
from torch.autograd import Variable
from zero import ProxyObject, serializer_table


def model_train(
    epochs: int,
    X: Type[ProxyObject],
    Y: Type[ProxyObject],
    learn_rate: float,
    model: torch.nn.Module,
    model_type: str,
    criterion: str,
    optimizer: str,
) -> torch.nn.Module:
    """
    Runs the ModelTrain function
    :param: epochs: The number of epochs to run training for
    :type: Integer
    :param: X: The input data
    :type: DataFrame
    :param: X: The output data
    :type: DataFrame
    :param: learn_rate: the learn rate ofthe model
    :type: Float
    :param: model: the model to be trained
    :type: torch.nn.Module
    :param: criterion: the evaluation metric of the model
    :type: criterion: String
    :param: optimizer: the optimisation method of the model
    :type: criterion: String
    :return: The trained model
    :type: torch.nn.Module
    """
    model = load_model_dict(model, model_type)
    if len(X.shape) == 1:
        X = X.series
    else:
        X = X.frame
    if len(Y.shape) == 1:
        Y = Y.series
    else:
        Y = Y.frame

    if ModelUtility.check_valid_model(model):
        model = ModelUtility.get_clean_model(model)
        if model == 0:
            print("Invalid model presented")
            return 0
    else:
        return 0

    criterion = get_criterion(criterion)
    optimizer = get_optimizer(model, learn_rate, optimizer)

    for epoch in range(epochs):

        inputs = Variable(ModelUtility.dataframe_to_tensor(X))
        labels = Variable(ModelUtility.dataframe_to_tensor(Y))

        # Clear gradient buffers because we don't want any gradient from previous epoch to carry forward, dont want to cummulate gradients
        optimizer.zero_grad()

        # get output from the model, given the inputs
        outputs = model(inputs)

        # get loss for the predicted output
        loss = criterion(outputs, labels)

        # get gradients w.r.t to parameters
        loss.backward()

        # update parameters
        optimizer.step()

        # print("epoch {}, loss {}".format(epoch, loss.item()))

    return serializer_table[str(torch.nn.Module)](model)


# TODO: fancy ref filtering
def get_criterion(
    criterion: String,
) -> torch.nn.Module:
    """
    set the loss function of the model

    :param criterion: loss function criterion
    :type criterion: String
    :return: loss function
    :rtype: torch.nn.Module
    """
    if criterion == "MSELoss":
        return torch.nn.MSELoss()
    elif criterion == "BCELoss":
        return torch.nn.BCELoss()
    else:
        print("your loss function was not found")


# TODO: fancy ref filtering
def get_optimizer(
    model: torch.nn.Module,
    learn_rate: float,
    optimizer: String,
) -> torch.optim.Optimizer:
    """
    set the optimizer of the model

    :param model: model to be set
    :type model: torch.nn.Module
    :param learn_rate: learn rate
    :type learn_rate: float
    :param optimizer: optimizer type
    :type optimizer: String
    :return: optimizer
    :rtype: torch.optim.Optimizer
    """
    return torch.optim.SGD(model.parameters(), lr=learn_rate)
