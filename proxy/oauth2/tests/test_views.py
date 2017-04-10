from django.core.urlresolvers import reverse


def test_user_profile_proxy(signed_client):
    url = reverse('oauth2_provider_proxy:user_profile_proxy')
    response = signed_client.get(url)
    assert response.status_code == 401


def test_authorize_proxy(signed_client):
    url = reverse('oauth2_provider_proxy:authorize_proxy')
    response = signed_client.get(url)
    assert response.status_code == 302


def test_token_proxy(signed_client):
    url = reverse('oauth2_provider_proxy:token_proxy')
    response = signed_client.post(url)
    assert response.status_code == 400


def test_revoke_token_proxy(signed_client):
    url = reverse('oauth2_provider_proxy:revoke_token_proxy')
    response = signed_client.post(url)
    assert response.status_code == 400
