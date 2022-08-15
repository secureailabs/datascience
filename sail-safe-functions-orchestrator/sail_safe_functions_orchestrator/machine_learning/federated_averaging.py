from tokenize import String
from typing import List
from pandas import DataFrame
from sail_safe_functions.machine_learning.ModelTrain import ModelTrain
from sail_safe_functions.machine_learning.ModelAverage import ModelAverage
from sail_safe_functions.machine_learning.ModelRetrieve import ModelRetrieve
import torch


def federated_averaging(
    epochs: int,
    federal_epochs: int,
    data_federation: List[DataFrame],
    X_col: List[str],
    Y_col: List[str],
    learn_rate: float,
    starting_model: torch.nn.Module,
    criterion: String,
    optimizer: String,
) -> torch.nn.Module:

    avg_model = starting_model

    # Train a model with every member of our data federation
    for epoch in range(federal_epochs):
        trained_models = []
        for j in range(len(data_federation)):
            trained_models.append(
                ModelTrain.run(
                    epochs,
                    data_federation[j][X_col],
                    data_federation[j][Y_col],
                    learn_rate,
                    avg_model,
                    criterion,
                    optimizer,
                )
            )
        avg_model = ModelAverage.run(trained_models)

        avg_model = ModelRetrieve.run(avg_model)

    return avg_model
