import torch


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
