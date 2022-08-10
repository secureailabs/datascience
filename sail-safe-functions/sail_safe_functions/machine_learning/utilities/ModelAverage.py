from sail_safe_functions.machine_learning.utilities.ModelUtility import ModelUtility


class ModelAverage:
    def run(models):

        model_parameters = []
        for model in models:
            model_parameters.append(ModelUtility.get_parameters_as_tensor(model))

        model_sum = 0.0
        for param in model_parameters:
            model_sum += param
        model_param_avg = model_sum / len(model_parameters)

        clean_model = ModelUtility.get_clean_model(models[0])

        if clean_model != 0:
            return ModelUtility.set_parameters_from_tensor(clean_model, model_param_avg)
        else:
            print("Problem while averaging the model")
            return 0
