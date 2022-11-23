import torch
from helper_libs.scn_side.machine_learning.ModelUtility import ModelUtility
from pandas import DataFrame
from sail_safe_functions.safe_function_base import SafeFunctionBase
from torch.autograd import Variable


class ModelTrain(SafeFunctionBase):
    """
    Trains a model on local data
    """

    def run(
        epochs: int,
        X: DataFrame,
        Y: DataFrame,
        learn_rate: float,
        model: torch.nn.Module,
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
        :type: criterion: str
        :param: optimizer: the optimisation method of the model
        :type: criterion: str
        :return: The trained model
        :type: torch.nn.Module
        """
        if ModelUtility.check_valid_model(model):
            model = ModelUtility.get_clean_model(model)
            if model == 0:
                print("Invalid model presented")
                return 0
        else:
            return 0

        criterion = ModelTrain.get_criterion(criterion)
        optimizer = ModelTrain.get_optimizer(model, learn_rate, optimizer)

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

        return model

    # TODO: fancy ref filtering
    @staticmethod
    def get_criterion(criterion: str) -> torch.nn.Module:
        if criterion == "MSELoss":
            return torch.nn.MSELoss()
        elif criterion == "BCELoss":
            return torch.nn.BCELoss()
        else:
            print("your loss function was not found")

    # TODO: fancy ref filtering
    @staticmethod
    def get_optimizer(model: torch.nn.Module, learn_rate: float, optimizer: str) -> torch.optim.Optimizer:
        return torch.optim.SGD(model.parameters(), lr=learn_rate)
