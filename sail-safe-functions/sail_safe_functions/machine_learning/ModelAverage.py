class ModelAverage:
    def run(model_parameters):

        model_sum = 0.0
        for param in model_parameters:
            model_sum += param
        model_param_avg = model_sum / len(model_parameters)

        return model_param_avg
