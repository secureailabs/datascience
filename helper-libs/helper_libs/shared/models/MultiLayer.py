import torch


class MultiLayer(torch.nn.Module):
    """
    A SAFE Logistic Regression Model. Parameters have been restricted in order to harden security posture.
    """

    # TODO: Add more parameters for model
    def __init__(self, layers):
        """
        Constructor for SAFE Logistic Model

        :param: inputSize: The number of inputs leading into the Logistic model.
        :type: Integer
        :param outputSize: The number of outputs the model will create for any set of input data
        :type: Integer
        :param: bias: Optional; whether the model will have a bias
        :type: bias: Boolean
        """
        super(MultiLayer, self).__init__()
        self.layers = layers

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        The forward function of the model

        :param: x: The input data
        :type: torch.Tensor
        :return: out: Model predictions based on x data
        :type: torch.Tensor
        """

        for layer in self.layers:
            x = layer(x)

        return x
