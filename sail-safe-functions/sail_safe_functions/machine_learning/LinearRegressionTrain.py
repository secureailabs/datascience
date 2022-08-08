import torch
from torch.nn import functional as F
from sail_safe_functions.machine_learning.LinearRegressionRetrieve import (
    LinearRegressionRetrieve,
)


class LinearRegressionTrain:
    # def _init_(self):
    #     print("Done")
    def run(
        in_layer,
        out_layer,
        epochs,
        data,
        learn_rate,
        starting_model,
        criterion,
        optimizer,
    ):
        # TODO: Enforce whitelisted models
        if not isinstance(starting_model, torch.Tensor):
            starting_model = (
                LinearRegressionTrain.get_parameters_as_tensor(starting_model),
            )

        model = LinearRegressionTrain.LinearRegression(
            in_layer,
            out_layer,
            criterion,
            optimizer,
            learn_rate,
        )
        model = LinearRegressionTrain.set_parameters_from_tensor(model, starting_model)
        LinearRegressionTrain.train_model(model, epochs, data[0], data[1])

        return LinearRegressionTrain.get_parameters_as_tensor(model)

    class LinearRegression(torch.nn.Module):
        # TODO: Add more parameters for model
        def __init__(self, in_layer, out_layer, criterion, optimizer, learn_rate):
            super(LinearRegressionTrain.LinearRegression, self).__init__()
            self.Linear = torch.nn.Linear(in_layer, out_layer, bias=False)

            # TODO: Input validation for standard types
            self.criterion = torch.nn.MSELoss(size_average=False)
            self.optimizer = torch.optim.SGD(self.Linear.parameters(), lr=learn_rate)
            # TODO: Input (end) validation for standard types

            self.learn_rate = learn_rate

        def forward(self, x):
            y_pred = self.Linear(x)
            return y_pred

    @staticmethod
    def train_model(model, epochs, x_data, y_data):
        for epoch in range(epochs):
            # Set model ready to train
            model.Linear.train()
            model.optimizer.zero_grad()
            # Forward pass
            y_pred = model.Linear(x_data)
            # Compute Loss
            loss = model.criterion(y_pred, y_data)
            # Backward pass
            loss.backward()
            model.optimizer.step()
        print(
            "Model Parameters: "
            + str(LinearRegressionTrain.get_parameters_as_tensor(model))
        )
        print("Loss: " + str(loss.data.view(-1)))

    @staticmethod
    def set_parameters_from_tensor(model, weights: torch.Tensor):
        if not isinstance(weights, torch.Tensor):
            print("Converting weights to tensor type")
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

    @staticmethod
    def get_parameters_as_tensor(model):
        params = [param.data.view(-1) for param in model.parameters()]
        params = torch.cat(params)
        params = params.cpu()
        return params
