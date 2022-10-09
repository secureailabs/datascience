from tokenize import String
from typing import List

import torch
from pandas import DataFrame
from zero import serializer_table

from .client import model_average_client, model_retrieve_client, model_train_client
from .model_utils import load_model_dict


def federated_averaging(
    clients: List,
    epochs: int,
    federal_epochs: int,
    data_federation: List[DataFrame],
    X_col: List[str],
    Y_col: List[str],
    learn_rate: float,
    starting_model: torch.nn.Module,
    model_type: str,
    criterion: String,
    optimizer: String,
) -> torch.nn.Module:
    """
    Runs federted averaging over a data federation.

    :param: epochs: number of epochs to train for on each local SCN
    :type: int
    :param: federal_epochs: Number of rounds fo averaging to run for
    :type: int
    :param: data_federation: a set of Dataframes representing the data federation
    :type: List[DataFrame]
    :param: X_col: A list ofcolumn names to be used for input data
    :type: List[String]
    :param: X_col: A list ofcolumn names to be used for label data
    :type: List[String]
    :param: learn_rate: the learn rate to train with
    :type: learn_rate: float
    :param: starting_model: The model at the start of training
    :type: torch.nn.Module
    :param: criterion: the evaluation metric to be used by each model
    :type: String
    :param: optimizer: The optimization method to be used by each model
    :type: String
    :return: Model after training with federated averaging
    :type: torch.nn.Module
    """

    avg_model = starting_model
    avg_model = serializer_table[str(torch.nn.Module)](avg_model)

    # Train a model with every member of our data federation
    for epoch in range(federal_epochs):
        trained_models = []
        for j in range(len(data_federation)):
            remote_model = model_train_client(
                epochs,
                clients[j],
                data_federation[j][X_col],
                data_federation[j][Y_col],
                learn_rate,
                avg_model,
                model_type,
                criterion,
                optimizer,
            )
            trained_models.append(remote_model)
        avg_model = model_average_client(clients[0], trained_models, model_type)

        avg_model = model_retrieve_client(clients[0], avg_model, model_type)

    avg_model = load_model_dict(avg_model, model_type)

    return avg_model
