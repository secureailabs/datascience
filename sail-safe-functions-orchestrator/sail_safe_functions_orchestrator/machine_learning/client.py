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
    return client.call("model_train", epochs, X, y, learn_rate, avg_model, model_type, criterion, optimizer)


def model_average_client(
    client,
    trained_models,
    model_type,
):
    return client.call("model_average", trained_models, model_type)


def model_retrieve_client(
    client,
    avg_model,
    model_type,
):
    return client.call("model_retrieve", avg_model, model_type)
