from helper_libs.shared.models.LogisticRegression import (
    LogisticRegression,
)
from helper_libs.shared.models.LinearRegression import (
    LinearRegression,
)
import torch


class ModelUtility:
    # set the parameters from a serialised model of equal shape
    @staticmethod
    def set_parameters_from_tensor(model, weights: torch.Tensor):
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
    def get_parameters_as_tensor(model):
        params = [param.data.view(-1) for param in model.parameters()]
        params = torch.cat(params)
        return params

    # return our current privacy parameter
    @staticmethod
    def get_epsilon(data):
        # return data.epsilon
        return 0.1

    @staticmethod
    def check_valid_model(model):

        # TODO: make checks for all our supported models
        if isinstance(model, LinearRegression):
            return True
        elif isinstance(model, LogisticRegression):
            return True
        else:
            print("model check Failed")
            return False

    @staticmethod
    def get_clean_model(model):
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
