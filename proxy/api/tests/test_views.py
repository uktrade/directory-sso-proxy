from django.core.urlresolvers import reverse


def test_session_user_proxy(client):
    response = client.get(reverse('session_user_proxy'))
    assert response.status_code == 403


def test_last_login_proxy(client):
    response = client.get(reverse('last_login_proxy'))
    assert response.status_code == 403
