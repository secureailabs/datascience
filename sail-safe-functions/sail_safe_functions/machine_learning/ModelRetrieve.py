import torch
from sail_safe_functions.machine_learning.ModelUtility import ModelUtility, load_model_dict
from zero import serializer_table


def model_retrieve(
    avg_model: dict,
    model_type: str,
    max_epsilon: float = 1.0,
) -> torch.nn.Module:
    """
    Runs ModelRetrieve function
    :param: avg_model: model to be retrieved back to the orchestrator
    :type: avg_model: torch.nn.Module
    :param: max_epsilon: the maximum mount of epsilon we will allow to leave
    :type: Float
    :return: model local to the orchestrator
    :type: torch.nn.Module
    """
    avg_model = load_model_dict(avg_model, model_type)

    # Check Privacy Parameter
    if ModelUtility.get_epsilon(avg_model) > max_epsilon:
        return "Epislon Budget Exceeded"

    # Clean the model
    clean_model = ModelUtility.get_clean_model(avg_model)
    if clean_model != 0:
        avg_model = ModelUtility.get_parameters_as_tensor(avg_model)
        clean_model = ModelUtility.set_parameters_from_tensor(clean_model, avg_model)
    else:
        print("Problem while retrieving the model")
        return 0

    clean_model = serializer_table[str(torch.nn.Module)](clean_model)
    return clean_model
