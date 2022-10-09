def add_noise_to_dataset_client(
    client,
    dataset,
    schema,
    noise_scale,
    cat_swap_frequency,
):
    """
    client side function to add noise to data

    :param client: _description_
    :type client: _type_
    :param dataset: _description_
    :type dataset: _type_
    :param schema: _description_
    :type schema: _type_
    :param noise_scale: _description_
    :type noise_scale: _type_
    :param cat_swap_frequency: _description_
    :type cat_swap_frequency: _type_
    :return: _description_
    :rtype: _type_
    """
    return client.call("add_noise_to_dataset_client", dataset, schema, noise_scale, cat_swap_frequency)
