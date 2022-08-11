from helper_libs.scn_side.machine_learning.ModelUtility import ModelUtility


class ModelAverage:
    def run(models, verbose=False):

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
            return ModelUtility.set_parameters_from_tensor(clean_model, model_param_avg)
        else:
            print("Problem while averaging the model")
            return 0
