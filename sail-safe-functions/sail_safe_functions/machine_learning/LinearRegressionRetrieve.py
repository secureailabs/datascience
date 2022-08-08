import torch
from torch.nn import functional as F


class LinearRegressionRetrieve:
    def run(
        in_layer,
        out_layer,
        learn_rate,
        criterion,
        optimizer,
        avg_model,
    ):
        model = LinearRegressionRetrieve.LinearRegression(
            in_layer, out_layer, criterion, optimizer, learn_rate, avg_model
        )

        LinearRegressionRetrieve.set_parameters_from_tensor(model, avg_model)

        return model

    class LinearRegression(torch.nn.Module):
        # TODO: Add more parameters for model
        def __init__(
            self, in_layer, out_layer, criterion, optimizer, learn_rate, avg_model
        ):
            super(LinearRegressionRetrieve.LinearRegression, self).__init__()
            self.Linear = torch.nn.Linear(in_layer, out_layer, bias=False)
            # self.set_parameters_from_tensor(avg_model)

            # TODO: Input validation for standard types
            self.criterion = torch.nn.MSELoss(size_average=False)
            self.optimizer = torch.optim.SGD(self.Linear.parameters(), lr=learn_rate)
            # TODO: Input (end) validation for standard types

            self.learn_rate = learn_rate

        def forward(self, x):
            y_pred = self.Linear(x)
            return y_pred

        def train_model(self, epochs, x_data, y_data):
            for epoch in range(epochs):
                # Set model ready to train
                self.Linear.train()
                self.optimizer.zero_grad()
                # Forward pass
                y_pred = self.Linear(x_data)
                # Compute Loss
                loss = self.criterion(y_pred, y_data)
                # Backward pass
                loss.backward()
                self.optimizer.step()
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

    @staticmethod
    def get_parameters_as_tensor(model):
        params = [param.data.view(-1) for param in model.parameters()]
        params = torch.cat(params)
        params = params.cpu()
        return params
