import pytest
from sail_aggregator_client import Client, SyncOperations


@pytest.mark.active
def test_client_instantiation():

    # Arrange
    client = Client(base_url="http://localhost:8000", verify_ssl=False, raise_on_unexpected_status=False, timeout=30.5)
    operation = SyncOperations(client=client)

    # Act

    # Assert
    assert type(operation) == SyncOperations
