from unittest.mock import patch

import pytest


@pytest.fixture
def signed_client(client):
    stub = patch(
        'config.signature.sso_client_checker.test_signature', return_value=True
    )
    stub.start()
    yield client
    stub.stop()
