from django.core.urlresolvers import reverse


def test_session_user_proxy(signed_client):
    response = signed_client.get(reverse('session_user_proxy'))
    # 404 because the request does not provide a valid
    # session key in the querystring for retrieving the session user
    assert response.status_code == 404


def test_session_user_bad_signature(client):
    response = client.get(reverse('session_user_proxy'))
    assert response.status_code == 403


def test_last_login_proxy(signed_client):
    response = signed_client.get(reverse('last_login_proxy'))
    assert response.status_code == 200


def test_last_login_proxy_bad_signature(client):
    response = client.get(reverse('last_login_proxy'))
    assert response.status_code == 403
