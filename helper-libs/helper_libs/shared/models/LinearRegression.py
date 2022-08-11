import torch


class LinearRegression(torch.nn.Module):
    # TODO: Add more parameters for model
    def __init__(self, inputSize, outputSize, bias=False):

        super(LinearRegression, self).__init__()
        self.model = torch.nn.Linear(inputSize, outputSize, bias=False)

    def forward(self, x):
        out = self.model(x)
        return out
