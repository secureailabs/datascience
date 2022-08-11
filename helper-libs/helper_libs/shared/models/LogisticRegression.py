import torch


class LogisticRegression(torch.nn.Module):
    # TODO: Add more parameters for model
    def __init__(self, inputSize, outputSize, bias=False):
        super(LogisticRegression, self).__init__()
        self.model = torch.nn.Linear(inputSize, outputSize, bias)

    def forward(self, x):
        out = self.model(x)
        out = torch.sigmoid(out)
        return out
