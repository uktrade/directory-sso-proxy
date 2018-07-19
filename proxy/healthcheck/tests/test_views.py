from django.core.urlresolvers import reverse


def test_health_check_proxy(client):
    response = client.get(
        reverse('database_health_check_proxy'), {'token': 'debug'}
    )
    assert response.status_code == 200


def test_ping_proxy_proxy(client):
    response = client.get(reverse('ping_proxy'))
    assert response.status_code == 200
