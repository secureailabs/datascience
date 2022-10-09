def model_train_client(
    epochs,
    client,
    X,
    y,
    learn_rate,
    avg_model,
    model_type,
    criterion,
    optimizer,
):
    """
    client side function for model train

    :param epochs: _description_
    :type epochs: _type_
    :param client: _description_
    :type client: _type_
    :param X: _description_
    :type X: _type_
    :param y: _description_
    :type y: _type_
    :param learn_rate: _description_
    :type learn_rate: _type_
    :param avg_model: _description_
    :type avg_model: _type_
    :param model_type: _description_
    :type model_type: _type_
    :param criterion: _description_
    :type criterion: _type_
    :param optimizer: _description_
    :type optimizer: _type_
    :return: _description_
    :rtype: _type_
    """
    return client.call("model_train", epochs, X, y, learn_rate, avg_model, model_type, criterion, optimizer)


def model_average_client(
    client,
    trained_models,
    model_type,
):
    """
    client side function for model average

    :param client: _description_
    :type client: _type_
    :param trained_models: _description_
    :type trained_models: _type_
    :param model_type: _description_
    :type model_type: _type_
    :return: _description_
    :rtype: _type_
    """
    return client.call("model_average", trained_models, model_type)


def model_retrieve_client(
    client,
    avg_model,
    model_type,
):
    """
    client side function for model retrieve

    :param client: _description_
    :type client: _type_
    :param avg_model: _description_
    :type avg_model: _type_
    :param model_type: _description_
    :type model_type: _type_
    :return: _description_
    :rtype: _type_
    """
    return client.call("model_retrieve", avg_model, model_type)
