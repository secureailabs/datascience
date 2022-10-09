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


def load_model_dict(
    model_dict,
    model_type,
):
    """
    load state dict to torch model

    :param model_dict: state dict
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
