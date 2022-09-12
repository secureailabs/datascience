from helper_libs.shared.models.LogisticRegression import (
    LogisticRegression,
)
from helper_libs.shared.models.LinearRegression import (
    LinearRegression,
)
import torch
import pandas as pd


class ModelUtility:
    """A helper Library to be used on the SCN side to do common operations needed by different SAFE functions."""

    # set the parameters from a serialised model of equal shape
    @staticmethod
    def set_parameters_from_tensor(
        model: torch.nn.Module, weights: torch.Tensor
    ) -> torch.nn.Module:
        """Sets a model to the parameters supplied in tensor form.

        :param: model: Model whose parameters are to be set
        :type: torch.nn.Module
        :param: weights: Serialised model parameters
        :type: torch.Tensor
        :return: Model set to serialised parameters
        :type: torch.nn.Module
        """
        if not isinstance(weights, torch.Tensor):
            # print("Converting weights to tensor type")
            weights = torch.tensor(weights)
        current_index = 0
        for parameter in model.parameters():
            numel = parameter.data.numel()
            size = parameter.data.size()
            parameter.data.copy_(
                weights[current_index : current_index + numel].view(size)
            )
            current_index += 1
        return model

    # return a serialised version of the model
    @staticmethod
    def get_parameters_as_tensor(model: torch.nn.Module) -> torch.Tensor:
        """Serialises model parameters into tensor form

        :param: model: Model whose parameters are to be serialised
        :type: torch.nn.Module
        :return: params: Serialised model parameters
        :type: torch.Tensor
        """
        params = [param.data.view(-1) for param in model.parameters()]
        params = torch.cat(params)
        return params

    # return our current privacy parameter
    @staticmethod
    def get_epsilon(data: object) -> float:
        """Retrieves epsilon from given data
        TODO: Works with solution which has not been implemented

        :param: data: data item whose epsilon attribute is to be queried
        :type: data: Generic Safe Object with epsilon attribute
        :return: epsilon value
        :type: float
        """
        # return data.epsilon
        return 0.1

    @staticmethod
    def check_valid_model(model: torch.nn.Module) -> bool:
        """Checks whether the model is one of our supported models

        :param: model: Model to be checked
        :type: Torch.nn.Module
        :return: Whether the model is correct
        :type: Boolean"""

        # TODO: make checks for all our supported models
        if isinstance(model, LinearRegression):
            return True
        elif isinstance(model, LogisticRegression):
            return True
        else:
            print("model check Failed")
            return False

    @staticmethod
    def get_clean_model(model: torch.nn.Module) -> torch.nn.Module:
        """Returns a 'clean' version of the model supplied. One which is newly instantiated with only approved attributes and functions.

        :param: model: Model to be cleaned
        :type: torch.nn.Module
        :return: cleaned model
        :type: torch.nn.Module
        """
        if ModelUtility.check_valid_model(model):

            # TODO: enumerate all supported params for each model
            in_layer = model.model.in_features
            out_layer = model.model.out_features

            if isinstance(model, LinearRegression):
                return LinearRegression(in_layer, out_layer)
            elif isinstance(model, LogisticRegression):
                return LogisticRegression(in_layer, out_layer)
            else:
                print("Model cleaning failed.")
                return 0

    # TODO: Types hard coded for now
    @staticmethod
    def dataframe_to_tensor(data: pd.DataFrame) -> torch.Tensor:
        """Transforms a DataFrame to a tensor.

        :param: data: DataFrame to be transformed
        :type: pd.DataFrame
        :return: tensor: Tensor representation of input data
        :type: torch.Tensor
        """
        # if isinstance(data.values, numpy.ndarray):
        #     tensor = torch.from_numpy(data.values)
        if not isinstance(data.values, torch.Tensor):
            tensor = torch.Tensor(data.values).float()
        else:
            print("Problem transforming dataframe to tensor")
            return -1
        return tensor
