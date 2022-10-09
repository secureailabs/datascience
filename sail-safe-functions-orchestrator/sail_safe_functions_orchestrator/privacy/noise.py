def add_noise_to_dataset_client(
    client,
    dataset,
    schema,
    noise_scale,
    cat_swap_frequency,
):
    return client.call("add_noise_to_dataset_client", dataset, schema, noise_scale, cat_swap_frequency)
