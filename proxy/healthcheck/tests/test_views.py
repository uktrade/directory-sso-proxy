from django.core.urlresolvers import reverse


def test_health_check_proxy_signed(signed_client):
    response = signed_client.get(
        reverse('health_check_proxy'), {'token': 'debug'}
    )
    assert response.status_code == 200


def test_session_user_proxy_unsigned(client):
    response = client.get(reverse('session_user_proxy'))
    assert response.status_code == 403


def test_ping_proxy_proxy_signed(signed_client):
    response = signed_client.get(reverse('ping_proxy'))
    assert response.status_code == 200


def test_ping_proxy_proxy_unsigned(client):
    response = client.get(reverse('ping_proxy'))
    assert response.status_code == 403
