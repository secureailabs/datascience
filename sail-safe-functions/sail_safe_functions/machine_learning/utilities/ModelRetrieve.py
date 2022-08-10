from sail_safe_functions.machine_learning.utilities.ModelUtility import ModelUtility


class ModelRetrieve:
    def run(avg_model, max_epsilon=1):

        # Check Privacy Parameter
        if ModelUtility.get_epsilon(avg_model) > max_epsilon:
            return "Epislon BUdget Exceeded"

        # Clean the model
        clean_model = ModelUtility.get_clean_model(avg_model)
        if clean_model != 0:
            avg_model = ModelUtility.get_parameters_as_tensor(avg_model)
            clean_model = ModelUtility.set_parameters_from_tensor(
                clean_model, avg_model
            )
        else:
            print("Problem while retrieving the model")
            return 0

        return clean_model
