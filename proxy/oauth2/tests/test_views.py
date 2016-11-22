from django.core.urlresolvers import reverse


def test_user_profile_proxy(client):
    response = client.get(reverse('oauth2_provider_proxy:user_profile_proxy'))
    assert response.status_code == 401


def test_authorize_proxy(client):
    response = client.get(reverse('oauth2_provider_proxy:authorize_proxy'))
    assert response.status_code == 302


def test_token_proxy(client):
    response = client.post(reverse('oauth2_provider_proxy:token_proxy'))
    assert response.status_code == 400


def test_revoke_token_proxy(client):
    response = client.post(reverse('oauth2_provider_proxy:revoke_token_proxy'))
    assert response.status_code == 400
