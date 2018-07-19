from django.core.urlresolvers import reverse


def test_authorize_proxy(client):
    url = reverse('oauth2_provider_proxy:authorize_proxy')
    response = client.get(url)
    assert response.status_code == 302


def test_token_proxy(client):
    url = reverse('oauth2_provider_proxy:token_proxy')
    response = client.post(url)
    assert response.status_code == 400


def test_revoke_token_proxy(client):
    url = reverse('oauth2_provider_proxy:revoke_token_proxy')
    response = client.post(url, content_type='application/json')
    assert response.status_code == 400
