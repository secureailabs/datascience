import torch
from sail_safe_functions.common.machine_learning.model_utility import ModelUtility
from sail_safe_functions.safe_function_base import SafeFunctionBase


class ModelRetrieve(SafeFunctionBase):
    """
    Retrieves a given model back to the orchestrator
    """

    @staticmethod
    def run(model: torch.nn.Module, max_epsilon: float = 1.0) -> torch.nn.Module:
        """
        Runs ModelRetrieve function
        :param: model: model to be retrieved back to the orchestrator
        :type: model: torch.nn.Module
        :param: max_epsilon: the maximum mount of epsilon we will allow to leave
        :type: Float
        :return: model local to the orchestrator
        :type: torch.nn.Module
        """
        # Check Privacy Parameter
        if ModelUtility.get_epsilon(model) > max_epsilon:
            raise Exception("Epislon Budget Exceeded")  # TODO type exception

        # Clean the model
        clean_model = ModelUtility.get_clean_model(model)
        if clean_model != 0:
            average_tensor = ModelUtility.get_parameters_as_tensor(model)
            clean_model = ModelUtility.set_parameters_from_tensor(clean_model, average_tensor)
        else:
            print("Problem while retrieving the model")
            return 0

        return clean_model
