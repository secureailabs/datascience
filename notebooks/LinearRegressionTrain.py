import torch
from torch.nn import functional as F


class LinearRegressionTrain:
    # def _init_(self):
    #     print("Done")

    def run(
        in_layer,
        out_layer,
        epochs,
        data,
        learn_rate=0.1,
        criterion=None,
        optimizer=None,
        starting_model=None,
    ):
        # TODO: Input validation for standard types

        model = LinearRegression(in_layer, out_layer, criterion, optimizer)
        criterion = torch.nn.MSELoss(size_average=False)
        optimizer = torch.optim.SGD(model.linear.parameters(), lr=learn_rate)

        # if isinstance(starting_model, torch.nn.Module):
        #     model.set_parameters_from_tensor(
        #         self.get_parameters_as_tensor(starting_model)
        #     )

        model.set_parameters_from_tensor(starting_model)

        model.train_model(epochs, data[0], data[1])

        return model.get_parameters_as_tensor()

    class LinearRegression(torch.nn.Module):
        def __init__(self, in_layer, out_layer, criterion, optimizer):
            super(LinearRegressionTrain.LinearRegression, self).__init__()
            self.linear = torch.nn.Linear(in_layer, out_layer, bias=False)
            self.criterion = criterion
            self.optimizer = optimizer

        def forward(self, x):
            y_pred = self.linear(x)
            return y_pred

        def train_model(self, epochs, x_data, y_data):
            for epoch in range(epochs):
                # Set model ready to train
                self.linear.train()
                self.optimizer.zero_grad()
                # Forward pass
                y_pred = self.linear(x_data)
                # Compute Loss
                loss = self.criterion(y_pred, y_data)
                # Backward pass
                loss.backward()
                self.optimizer.step()
            print("Loss: " + str(loss.data.view(-1)))

        def set_parameters_from_tensor(self, weights: torch.Tensor):
            if not isinstance(weights, torch.Tensor):
                print("Converting weights to tensor type")
                weights = torch.tensor(weights)
            current_index = 0
            for parameter in self.parameters():
                numel = parameter.data.numel()
                size = parameter.data.size()
                parameter.data.copy_(
                    weights[current_index : current_index + numel].view(size)
                )
                current_index += 1

        def get_parameters_as_tensor(self):
            params = [param.data.view(-1) for param in self.parameters()]
            params = torch.cat(params)
            params = params.cpu()
            return params
