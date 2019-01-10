from django.conf import settings
from django.core.urlresolvers import reverse


def test_health_check_proxy(client):
    response = client.get(
        reverse('health_check_proxy'),
        {'token': settings.TEST_SSO_HEALTHCHECK_TOKEN}
    )
    assert response.status_code == 200


def test_ping_proxy_proxy(client):
    response = client.get(reverse('ping_proxy'))
    assert response.status_code == 200
