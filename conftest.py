from http.cookies import SimpleCookie

import pytest
from mohawk import Sender


@pytest.fixture
def authenticated_client(client, settings):
    sender = Sender(
        credentials={
            'id': settings.TEST_IP_RESTRICTOR_SKIP_SENDER_ID,
            'key': settings.TEST_IP_RESTRICTOR_SKIP_SENDER_SECRET,
            'algorithm': 'sha256',
        },
        url='/',
        method='',
        always_hash_content=False,
    )
    client.cookies = SimpleCookie({'ip-restrict-signature': sender.request_header})
    return client
