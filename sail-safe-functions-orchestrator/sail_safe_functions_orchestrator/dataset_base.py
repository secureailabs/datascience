class DatasetBase:
    def __init__(
        self,
        dataset_federation_id: str,
        dataset_federation_name: str,
        dataset_id: str,
        dataset_name: str,
    ) -> None:
        self.dataset_federation_id = dataset_federation_id
        self.dataset_federation_name = dataset_federation_name
        self.dataset_id = dataset_id
        self.dataset_name = dataset_name
