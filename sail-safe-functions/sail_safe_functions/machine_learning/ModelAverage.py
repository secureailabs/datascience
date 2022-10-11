from typing import Tuple

import torch
from sail_safe_functions.machine_learning.ModelUtility import ModelUtility, load_model_dict
from zero import serializer_table


def model_average(
    models: Tuple[dict],
    model_type: str,
    verbose: bool = False,
) -> torch.nn.Module:
    """
    Runs the ModelAvg safe funciton
    :param: models: A list of models which are to be averaged
    :type: models: List[torch.nn.Module]
    :param: verbose: whether to print out a limited amount of information
    :type: Boolean
    :return: fresh model with parameters set to the average
    :type: torch.nn.Module
    """
    models = list(models)
    for i in range(len(models)):
        models[i] = load_model_dict(models[i], model_type)

    model_parameters = []
    for model in models:
        model_parameters.append(ModelUtility.get_parameters_as_tensor(model))
        if verbose:
            print(model_parameters[-1])

    model_sum = 0.0
    for param in model_parameters:
        model_sum += param
    model_param_avg = model_sum / len(model_parameters)

    if verbose:
        print(model_param_avg)

    clean_model = ModelUtility.get_clean_model(models[0])

    if clean_model != 0:
        if verbose:
            print("Model Successfully Averaged")
        res = ModelUtility.set_parameters_from_tensor(clean_model, model_param_avg)
        return serializer_table[str(torch.nn.Module)](res)
    else:
        print("Problem while averaging the model")
        return 0
