import pandas as pd
import torch
from zero import deserializer_table


class LinearRegression(torch.nn.Module):
    """
    An SAFE Linear Regression Model. Parameters have been restricted in order to harden security posture.
    """

    # TODO: Add more parameters for model
    def __init__(self, inputSize, outputSize, bias=False):
        """
        Constructor for SAFE Linear Model

        :param: inputSize: The number of inputs leading into the Linear model.
        :type: Integer
        :param outputSize: The number of outputs the model will create for any set of input data
        :type: Integer
        :param: bias: Optional; whether the model will have a bias
        :type: bias: Boolean
        """
        super(LinearRegression, self).__init__()
        self.model = torch.nn.Linear(inputSize, outputSize, bias=False)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        The forward function of the model

        :param: x: The input data
        :type: torch.Tensor
        :return: out: Model predictions based on x data
        :type: torch.Tensor
        """
        out = self.model(x)
        return out


class LogisticRegression(torch.nn.Module):
    """
    A SAFE Logistic Regression Model. Parameters have been restricted in order to harden security posture.
    """

    # TODO: Add more parameters for model
    def __init__(self, inputSize, outputSize, bias=False):
        """
        Constructor for SAFE Logistic Model

        :param: inputSize: The number of inputs leading into the Logistic model.
        :type: Integer
        :param outputSize: The number of outputs the model will create for any set of input data
        :type: Integer
        :param: bias: Optional; whether the model will have a bias
        :type: bias: Boolean
        """
        super(LogisticRegression, self).__init__()
        self.model = torch.nn.Linear(inputSize, outputSize, bias)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        The forward function of the model

        :param: x: The input data
        :type: torch.Tensor
        :return: out: Model predictions based on x data
        :type: torch.Tensor
        """
        out = self.model(x)
        out = torch.sigmoid(out)
        return out


class ModelUtility:
    """
    A helper Library to be used on the SCN side to do common operations needed by different SAFE functions.
    """

    # set the parameters from a serialised model of equal shape
    @staticmethod
    def set_parameters_from_tensor(model: torch.nn.Module, weights: torch.Tensor) -> torch.nn.Module:
        """
        Sets a model to the parameters supplied in tensor form.

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
            parameter.data.copy_(weights[current_index : current_index + numel].view(size))
            current_index += 1
        return model

    # return a serialised version of the model
    @staticmethod
    def get_parameters_as_tensor(model: torch.nn.Module) -> torch.Tensor:
        """
        Serialises model parameters into tensor form

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
        """
        Retrieves epsilon from given data
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
        """
        Checks whether the model is one of our supported models

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
        """
        Returns a 'clean' version of the model supplied. One which is newly instantiated with only approved attributes and functions.

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


def load_model_dict(
    model_dict,
    model_type,
):
    """
    load model from state dict

    :param model_dict: model state dict
    :type model_dict: dict
    :param model_type: model type
    :type model_type: str
    :return: torch model
    :rtype: torch.nn.Module
    """
    model_dict = deserializer_table[str(torch.nn.Module)](model_dict)
    size = list(model_dict["model.weight"].size())
    if len(size) == 1:
        input_size = 1
        output_size = 1
    else:
        output_size, input_size = size

    model = 0
    if model_type == "linear_regression":
        model = LinearRegression(input_size, output_size)
    elif model_type == "logistic_regression":
        model = LogisticRegression(input_size, output_size)
    else:
        raise Exception("model not supported by deserializer")
    model.load_state_dict(model_dict)
    return model
